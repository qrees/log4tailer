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


import os
import time
import sys
from log4tailer.Message import Message
from log4tailer.Log import Log
from log4tailer.reporting import Resume
from log4tailer.Configuration import MailConfiguration
from log4tailer import notifications

class LogTailer:
    '''Tails the log provided by Log class'''
    def __init__(self,logcolors, target, pause, throttleTime, silence, actions, properties):
        self.arrayLog = []
        self.logcolors = logcolors
        self.pause = pause
        self.silence = silence
        self.actions = actions
        self.throttleTime = throttleTime 
        self.target = target
        self.properties = properties
        self.mailAction = None

    def addLog(self,log):
        self.arrayLog.append(log)
    
    def __printHeaderLog(self,path):
        print "==> "+path+" <=="

    def posEnd(self):
        '''Open the logs and position the cursor
        to the end'''
        for log in self.arrayLog:
            log.openLog()
            log.seekLogNearlyEnd()

    def __initialize(self,message):
        '''prints the last 10 
        lines for each log, one log 
        at a time'''
        printAction = notifications.Print()
        lenarray = len(self.arrayLog)
        cont = 0
        for log in self.arrayLog:
            cont += 1
            self.__printHeaderLog(log.getLogPath())
            line = log.readLine()
            while line != '':
                line = line.rstrip()
                message.parse(line, log)
                printAction.printInit(message)
                line = log.readLine()
            # just to emulate the same behaviour as tail
            if cont < lenarray:
                print

    def hasRotated(self,log):
        """Returns True if log has rotated
        False otherwise"""
        if log.getcurrInode()!=log.inode or log.getcurrSize()<log.size: 
            print "Log "+log.path+" has rotated"
            # close the log and open it again 
            log.closeLog()
            log.openLog()
            log.seekLogEnd()
            return True
        return False

    def getTermLines(self):
        termlines = os.popen("tput lines")
        ttlines = termlines.readline()
        termlines.close()
        ttlines = int(ttlines)
        return ttlines

    def printLastNLines(self,n):
        '''tail -n numberoflines method in pager mode'''
        message = Message(self.logcolors)
        action = notifications.Print()
        for log in self.arrayLog:
            fd = log.openLog()
            numlines = log.numLines()
            pos = numlines-n
            count = 0
            buff = []
            ttlines = self.getTermLines()
            for curpos,line in enumerate(fd):
                if curpos >= pos:
                    line = line.rstrip()
                    message.parse(line, log)
                    action.notify(message, log)
                    count += 1
                    buff.append(line)
                    if count%ttlines == 0:
                        cont = raw_input("continue\n")
                        count = 0
                        ttlines = self.getTermLines()
            log.closeLog()

    def daemonize (self, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        try:
            pid = os.fork( )
            if pid > 0:
                sys.exit(0) 
        except OSError, e:
            sys.stderr.write("first fork failed: (%d) %s\n" % (e.errno, e.strerror))
            sys.exit(1)
        os.chdir("/")
        os.umask(0)
        os.setsid( )
        try:
            pid = os.fork( )
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("second fork failed: (%d) %s\n" % (e.errno, e.strerror))
            sys.exit(1)
        print "daemonized"
        for f in sys.stdout, sys.stderr: f.flush()
        si = file(stdin, 'r')
        so = file(stdout, 'a+')
        se = file(stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    
    def pipeOut(self):
        """Reads from standard input 
        and prints to standard output"""
        message = Message(self.logcolors,self.target,self.properties)
        stdin = sys.stdin
        anylog = Log('anylog')
        for line in stdin:
            message.parse(line, anylog)
            for action in self.actions:
                action.notify(message, anylog)
    
    def __getAction(self,module):
        for action in self.actions:
            if isinstance(action,module):
                return action
        return None

    def mailIsSetup(self):
        '''check if mail properties
        already been setup'''
        properties = self.properties
        action = self.__getAction(notifications.Mail)
        if action:
            self.mailAction = action
            return True
        if properties:
            if properties.getValue('inactivitynotification') == 'mail':
                # check if there is any inactivity action actually setup
                inactivityaction = self.__getAction(notifications.Inactivity)
                if inactivityaction:
                    self.mailAction = inactivityaction.getMailAction()
                    return True
        return False
    
    def resumeBuilder(self):
        resume = Resume(self.arrayLog)
        notify_defaults = ('mail', 'print')
        properties = self.properties
        if properties:
            notification_type = properties.getValue('analyticsnotification')
            analyticsgap = properties.getValue('analyticsgaptime')
            if notification_type and notification_type not in notify_defaults:
                resume.notification_type(notification_type)
            elif notification_type == 'mail':
                if not self.mailIsSetup():
                    mailAction = MailConfiguration.setupMailAction()
                    resume.setMailNotification(mailAction)
                else:
                    resume.setMailNotification(self.mailAction)
            if analyticsgap:
                resume.setAnalyticsGapNotification(analyticsgap)
        return resume
    
    def notifyActions(self, message, log):
        for action in self.actions:
            action.notify(message, log)

    def tailer(self):
        '''Stdout multicolor tailer'''
        message = Message(self.logcolors,self.target,self.properties)
        resume = self.resumeBuilder()
        self.posEnd()
        if self.silence:
            self.daemonize()
        try:
            self.__initialize(message)
            lastLogPathChanged = ""
            curpath = ""
            while True:
                found = 0
                time.sleep(self.throttleTime)
                for log in self.arrayLog:
                    changed = 0
                    curpath = log.getLogPath()
                    if self.hasRotated(log):
                        found = 0
                    lines = log.readLines()
                    if not lines:
                        # notify actions
                        message.parse('', log)
                        resume.update(message, log)
                        self.notifyActions(message, log)
                        continue
                    for line in lines:
                        found = 1
                        line = line.rstrip()
                        # to emulate the tail command
                        if curpath != lastLogPathChanged:
                            print
                            self.__printHeaderLog(log.getLogPath())
                        lastLogPathChanged = log.getLogPath()
                        message.parse(line, log)
                        resume.update(message, log)
                        self.notifyActions(message, log)
                    log.size = log.getcurrSize()
                if found == 0:
                    #sleep for 1 sec
                    time.sleep(self.pause)
        except KeyboardInterrupt:
            for log in self.arrayLog:
                log.closeLog()
            if self.mailAction:
                self.mailAction.quitSMTP()
            print "\n"
            resume.report()
            print "Ended log4tailer, because colors are fun"
