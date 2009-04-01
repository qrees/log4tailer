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

    def __init__(self,inactivityTime):
        self.inactivityTime = inactivityTime
        self.timer = Timer.Timer(inactivityTime)
        self.timer.startTimer()
        self.logColors = LogColors.LogColors()

    def triggerAction(self,message):
        if not message.getPlainMessage():
            if self.timer.ellapsed() > self.inactivityTime:
                # at this moment we will just print an emphasized alert in stdout
                print self.logColors.backgroundemph+"Inactivity in log"+self.logColors.reset
        # else if we got sth in message then, means we got 
        # some kind of activity, so do nothing




