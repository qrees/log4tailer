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
from log4tailer import TermColorCodes

class Resume:
    '''Will report of number of debug, info and warn 
    events. For Error and Fatal will provide the timestamp 
    if there was any event of that level'''

    def __init__(self,arrayLog):
        self.arrayLog = arrayLog
        self.initTime = time()
        self.logsReport = {}
        for log in arrayLog:
            self.logsReport[log.getLogPath()] = {'DEBUG':0,
                                                 'INFO':0,
                                                 'WARN':0,
                                                 'ERROR':[],
                                                 'FATAL':[]}

        self.nonTimeStamped = ['DEBUG','INFO','WARN']
        self.orderReport = ['FATAL','ERROR','WARN','INFO','DEBUG']

    def update(self,message,log):
        messageLevel = message.getMessageLevel()
        logPath = log.getLogPath()
        logKey = self.logsReport[logPath]
        if logKey.has_key(messageLevel):
            if messageLevel in self.nonTimeStamped:
                logKey[messageLevel] += 1
            else:
                logKey[messageLevel].append(strftime("%d %b %Y %H:%M:%S", localtime())
                        +'=>> '+message.getPlainMessage())

                #def getInfo(self,messageLevel):
       # return self.levels[messageLevel]

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

    def colorize(self,line,colors):
        return colors.backgroundemph+line+colors.reset

    def report(self):
        colors = TermColorCodes.TermColorCodes()
        print "Analytics: "
        print "Uptime: "
        print self.__execTime()
        for log in self.arrayLog:
            titleLog = self.colorize("Report for Log "+log.getLogPath(),colors)
            print titleLog
            print "Levels Report: "
            logKey = self.logsReport[log.getLogPath()]  
            for level in self.orderReport:
                print level+":"
                if level in self.nonTimeStamped:
                    print logKey[level]
                else:
                    for timestamp in logKey[level]:
                        print timestamp

                       
