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

import sys
from smtplib import *
from Timer import *

class MailAction:
    """Common actions to be taken
    by the Tailer"""

    def __init__(self, fro = None, to = None, hostname = None, user = None, passwd = None):
        self.fro = fro
        self.to = to
        self.hostname = hostname
        self.user = user
        self.passwd = passwd
        self.conn = None
        self.timer = Timer(5)
        self.timer.startTimer()

    def triggerAction(self,message):
        '''msg to print, send by email, whatever...'''
        fh = open('/home/jordilin/mailog','w')
        fh.write("got "+message.getPlainMessage())
        fh.close()
        body = message.getPlainMessage()
        #if message.getMessageLevel != 'FATAL':
        #    return
        msg = "Subject: Log4Tailer alert\r\nFrom: %s\r\nTo: %s\r\n\r\n" % (self.fro,self.to)+body
        try:
            if self.timer.ellapsed() < self.timer.end:
                return
            self.conn.sendmail(self.fro,self.to,msg)
        except:
            fh = open('/home/jordilin/mailogerror','w')
            fh.write("got "+message.getPlainMessage())
            fh.close()

            print "error sending email"
            self.conn.quit()
            sys.exit()
        return


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

    def printStdOut(self, line, log = None):
        if log:
            log.printa(line)




