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

class Message:
    '''the message to be actioned
    and showed being by email, stdout,...'''

    def __init__(self,logcolor,patarget = None):
        
        self.patarget = patarget
        self.color = logcolor
        self.plainMessage = None
        self.colorizedMessage = None
        self.colorparser = ColorParser()
        self.messageLevel = None
    

    def getColorizedMessage(self):
        if self.patarget:
            res = self.patarget.search(self.plainMessage)
            if res:
                return self.color.backgroundemph+self.plainMessage+self.color.reset
        
        # tail the other lines (levels)
        if self.messageLevel == "WARN":
            return self.color.warn+self.plainMessage+self.color.reset
        elif self.messageLevel == "FATAL":
            return self.color.fatal+self.plainMessage+self.color.reset
        elif self.messageLevel == "INFO":
            return self.color.info+self.plainMessage+self.color.reset
        elif self.messageLevel == "ERROR":
            return self.color.error+self.plainMessage+self.color.reset
        elif self.messageLevel == "DEBUG":
            return self.color.debug+self.plainMessage+self.color.reset
        else:
            return self.plainMessage


    def getMessageLevel(self):
        return self.messageLevel


    def getPlainMessage(self):
        return self.plainMessage
    
    def parse(self,line):
        '''Need to parse the line
        and check in what level we are in'''
        
        self.plainMessage = line
        self.messageLevel = self.colorparser.parse(line)
        
                

   
        
        

