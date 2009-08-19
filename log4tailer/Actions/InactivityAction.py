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
from log4tailer import Timer,LogColors

class InactivityAction:
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
            notification = properties.getValue(InactivityAction.InactivityActionNotification)
        self.notification = notification or 'print'

    def triggerAction(self,message,log):
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
    
