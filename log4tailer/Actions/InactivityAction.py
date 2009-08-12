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
        self.timer = Timer.Timer(inactivityTime)
        self.timer.startTimer()
        self.logColors = LogColors.LogColors()
        self.acumulativeTime = 0
        self.mailAction = None
        self.notification = 'print'
        if properties:
            self.notification = properties.getValue(InactivityAction.InactivityActionNotification)

    def triggerAction(self,message):
        if not message.getPlainMessage():
            ellapsedTime = self.timer.inactivityEllapsed()
            if ellapsedTime > float(self.inactivityTime):
                self.acumulativeTime += ellapsedTime
                messageAlert = "Inactivity in the log for "+ str(self.acumulativeTime) + " seconds"
                
                if self.notification == 'print':
                    print self.logColors.backgroundemph+messageAlert+self.logColors.reset
                elif self.notification == 'mail':
                    self.mailAction.setBodyMailAction(messageAlert)
                    self.mailAction.triggerAction(message)

                self.timer.reset()
        # else if we got sth in message then, means we got 
        # some kind of activity, so do nothing
        else:
            #start the timer again
            self.resetTimer()
            self.acumulativeTime = 0

    def getNotificationType(self):
        return self.notification

    def setMailNotification(self,mailAction):
        '''sets a mailAction for inactivityAction notification'''
        self.mailAction = mailAction
    
    def resetTimer(self):
        self.timer.reset()
