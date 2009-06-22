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

from time import time,localtime,strftime

class Resume:
    '''Will report of number of debug, info and warn 
    events. For Error and Fatal will provide the timestamp 
    if there was any event of that level'''

    def __init__(self):
        self.initTime = time()
        self.levels = {'DEBUG':0,
                       'INFO':0,
                       'WARN':0,
                       'ERROR':[],
                       'FATAL':[]}

        self.nonTimeStamped = ['DEBUG','INFO','WARN']
        self.orderReport = ['FATAL','ERROR','WARN','INFO','DEBUG']

    def update(self,message):
        messageLevel = message.getMessageLevel()
        if self.levels.has_key(messageLevel):
            if messageLevel in self.nonTimeStamped:
                self.levels[messageLevel] += 1
            else:
                self.levels[messageLevel].append(strftime("%d %b %Y %H:%M:%S", localtime())
                        +' '+message.getPlainMessage())

    def getInfo(self,messageLevel):
        return self.levels[messageLevel]

    def __hoursMinsFormat(self,secs):
        years, secs = divmod(secs, 31556926)
        mins, secs = divmod(secs, 60)
        hours, mins = divmod(mins, 60)
        days, hours = divmod(hours, 24)
        
        return str(years)+" years "+str(days)+" days "+ str(hours)+" hours "+ str(mins)+" mins "+str(secs)+" secs "

            
    def __execTime(self):
        finish = time()
        ellapsed = finish-self.initTime
        return self.__hoursMinsFormat(ellapsed)

    def report(self):
        print "Analytics: "
        print "Uptime: "
        print self.__execTime()
        print "Levels Report: "
        for level in self.orderReport:
            print level+":"
            if level in self.nonTimeStamped:
                print self.levels[level]
            else:
                for timestamp in self.levels[level]:
                    print timestamp

                       
