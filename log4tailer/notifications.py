# Log4Tailer: A multicolored python tailer for log4J logs
# Copyright (C) 2008 Jordi Carrillo Bosch

# This file is part of Log4Tailer Project.
#
# Log4Tailer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Log4Tailer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Log4Tailer.  If not, see <http://www.gnu.org/licenses/>.

import os, sys, time
import LogColors
from smtplib import *
import datetime

class Print(object):
    '''PrintAction: prints to stdout the 
    colorized log traces'''

    def __init__(self):
        pass
    
    def notify(self, message, log):
        '''msg should be colorized already
        there is a module in pypy colorize, check it out'''
        (pause, colormsg) = message.getColorizedMessage()
        if colormsg:
            print colormsg
            time.sleep(pause)

    def printInit(self, message):
        (pause,colormsg) = message.getColorizedMessage()
        pause = 0
        if colormsg:
            print colormsg

class Inactivity(object):
    '''sends an email or print
    alert in case too much inactivity
    in the log.
    This action must be triggered everytime 
    we scan in the log.'''

    InactivityActionNotification = 'inactivitynotification'

    def __init__(self,inactivityTime,properties=None):
        self.inactivityTime = inactivityTime
        self.logColors = LogColors.LogColors()
        self.acumulativeTime = 0
        self.mailAction = None
        notification = None
        if properties:
            notification = properties.getValue(Inactivity.InactivityActionNotification)
            self.logColors.parseConfig(properties)
        self.notification = notification or 'print'

    def notify(self,message,log):
        plainmessage, logpath = message.getPlainMessage()
        timer = log.getInactivityTimer()
        if not plainmessage:
            ellapsedTime = timer.inactivityEllapsed()
            if ellapsedTime > float(self.inactivityTime):
                log.setInactivityAccTime(ellapsedTime)
                messageAlert = "Inactivity in the log "+logpath+" for "+ str(log.getInactivityAccTime()) + " seconds"
                
                if self.notification == 'print':
                    print self.logColors.backgroundemph+messageAlert+self.logColors.reset
                elif self.notification == 'mail':
                    self.mailAction.setBodyMailAction(messageAlert)
                    self.mailAction.triggerAction(message,log)
                    self.mailAction.setBodyMailAction(None)
                timer.reset()
        # else if we got sth in message then, means we got 
        # some kind of activity, so do nothing
        else:
            #start the timer again
            timer.reset()
            log.setInactivityAccTime(0)
            ellapsedTime = 0

    def getNotificationType(self):
        return self.notification

    def setMailNotification(self,mailAction):
        '''sets a mailAction for inactivityAction notification'''
        self.notification = 'mail'
        self.mailAction = mailAction

    def getMailAction(self):
        return self.mailAction

class Mail(object):
    """Common actions to be taken
    by the Tailer"""
    
    mailLevels = ['ERROR','FATAL']
    weekdayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    monthname = [None,
                 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    def __init__(self, fro = None, to = None, hostname = None, user = None, passwd = None):
        self.fro = fro
        self.to = to
        self.hostname = hostname
        self.user = user
        self.passwd = passwd
        self.conn = None
        self.bodyMailAction = None

    def date_time(self):
        """
        Taken from logging.handlers SMTP python distribution
        
        Return the current date and time formatted for a MIME header.
        Needed for Python 1.5.2 (no email package available)
        """
        year, month, day, hh, mm, ss, wd, y, z = time.gmtime(time.time())
        s = "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (
                self.weekdayname[wd],
                day, self.monthname[month], year,
                hh, mm, ss)
        return s
        
    def getNow(self):
        try:
            from email.utils import formatdate
        except ImportError:
            formatdate = self.date_time
        return formatdate()
        
    def notify(self,message,log):
        '''msg to print, send by email, whatever...'''
        
        body = self.bodyMailAction
        if not body:
            if message.getMessageLevel() not in MailAction.mailLevels and not message.isATarget():
                return
            message, logpath = message.getPlainMessage()
            title = "Alert found for log "+logpath
            fancyheader = len(title)*'='
            body = fancyheader+"\n"
            body += title+"\n"
            body += fancyheader+"\n"
            body += message+"\n"

        now = self.getNow()
        
        msg = "Subject: Log4Tailer alert\r\nFrom: %s\r\nTo: %s\r\nDate: %s\r\n\r\n" % (self.fro,self.to,now)+ body
        timer = log.getMailTimer()
        try:
            if timer.awaitSend(log.getTriggeredNotSent()):
                log.setTriggeredNotSent(True)
                return
            self.conn.sendmail(self.fro,self.to,msg)
        except SMTPServerDisconnected:
            # server could have disconnected
            # after a long inactivity. Connect
            # again and send the corresponding 
            # alert
            self.connectSMTP()
            self.conn.sendmail(self.fro,self.to,msg)

        self.bodyMailAction = None
        log.setTriggeredNotSent(False)
        return

    def setBodyMailAction(self,body):
        self.bodyMailAction = body
    
    def sendNotificationMail(self,body):
        '''Sends a notification mail'''
        now = self.getNow()
        msg = "Subject: Log4Tailer Notification Message\r\nFrom: %s\r\nTo: %s\r\nDate: %s\r\n\r\n" % (self.fro,self.to,now)+ body
        try:
            self.conn.sendmail(self.fro,self.to,msg)
        except SMTPServerDisconnected:
            self.connectSMTP()
            self.conn.sendmail(self.fro,self.to,msg)

    def connectSMTP(self):
        try:
            conn = SMTP(self.hostname)
            conn.login(self.user,self.passwd)
            print "connected"
        except:
            print "Failed to connect "+self.hostname
            sys.exit()
        self.conn = conn

    def quitSMTP(self):
        try:
            self.conn.quit()
        except:
            print "failed to quit SMTP connection"
            sys.exit()
    
    def emailSendMail(self,to,fro,contents):
        #send email using SendMail
        return


class Filter(Print):
    """ When a pattern is found, it will notify 
    the user, otherwise nothing will be notified. It 
    would be a mix of tail and grep
    """

    def __init__(self, pattern):
        self.pattern = pattern
    
    def notify(self, message, log):
        plainMessage = message.plainMessage
        if not plainMessage:
            return
        if self.pattern.search(plainMessage):
            Print.notify(self, message, log)
