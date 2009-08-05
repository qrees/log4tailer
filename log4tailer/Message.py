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

from ColorParser import ColorParser
from Actions import PauseMode
import re

class Message:
    '''the message to be actioned
    and showed being by email, stdout,...'''

    def __init__(self,logcolor,target = None, properties = None):
        
        self.patarget = None
        self.isTarget = None
        if target:
            # user can provide multiple
            # comma separated targets
            target = self.__getMultipleTargets(target)
            self.patarget = re.compile(target)
        self.color = logcolor
        self.plainMessage = None
        self.colorizedMessage = None
        self.colorparser = ColorParser()
        self.messageLevel = None
        self.pauseMode = PauseMode.PauseMode()
        self.logOwnColor = False
        if properties:
            self.pauseMode.parseConfig(properties)
    
    def isATarget(self):
        if self.isTarget:
            return True
        return False

    def getColorizedMessage(self):
        '''it returns a tuple, first 
        element the pause associated 
        with the level found and second 
        element the colorized message
        This method is mainly used 
        by the PrintAction action'''

        if not self.plainMessage:
            return (0,'')
        
        # targets have priority over Levels
        if self.isTarget:
            return (self.pauseMode.getPause('target'),self.color.backgroundemph+self.plainMessage+self.color.reset)
        
        if self.logOwnColor:
            return (0,self.color.getLogColor(self.logOwnColor)
                    +self.plainMessage+self.color.reset)
   

        # tail the other lines (levels)
        levelcolor = ""
        if self.messageLevel == "WARN":
            levelcolor = self.color.warn
        elif self.messageLevel == "FATAL":
            levelcolor = self.color.fatal
        elif self.messageLevel == "INFO":
            levelcolor = self.color.info 
        elif self.messageLevel == "ERROR":
            levelcolor = self.color.error 
        elif self.messageLevel == "DEBUG":
            levelcolor = self.color.debug 
        else:
            return (0,self.plainMessage)

        return (self.pauseMode.getPause(self.messageLevel.lower()),levelcolor+self.plainMessage+self.color.reset)

        
    def __getMultipleTargets(self,target):
        target = target.replace(',','|')
        return target
    
    def getMessageLevel(self):
        return self.messageLevel


    def getPlainMessage(self):
        return self.plainMessage
    
    def __parseSetOpts(self,line):
        self.isTarget = None
        if line:
            self.plainMessage = line.rstrip()
            self.messageLevel = self.colorparser.parse(line)
            # is target?
            if self.patarget:
                self.isTarget = self.patarget.search(self.plainMessage)
            return
        # if we don't have anything in line
        # just set current Message to unknown
        
        self.plainMessage = None
        self.messageLevel = 'UNKNOWN'

    def parse(self,line,logOwnColor):
        '''Need to parse the line
        and check in what level we are in'''
        self.logOwnColor = logOwnColor
        self.__parseSetOpts(line)                
        

