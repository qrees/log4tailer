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



import os,re,sys
from stat import *

class Log:
    '''Class that defines a common
    structure in a log'''
    def __init__(self,path):
        self.path = path
        self.fh = None
        self.inode = None
        self.size = None
        self.loglevel = None

    def getcurrInode(self):
        try:
            inode = os.stat(self.path)[ST_INO]
        except:
            print "Could not stat, file removed?"
            print "exiting..."
            sys.exit()
        return inode

    def getcurrSize(self):
        size = os.stat(self.path)[ST_SIZE]
        return size
    
    def openLog(self):
        try:
            self.size = os.stat(self.path)[ST_SIZE]
            self.inode = os.stat(self.path)[ST_INO]
        except:
            print "file "+self.path+" does not exist"
            sys.exit()
        try:
            fd = open(self.path,'r')
            self.fh = fd
            return fd
        except:
            print "Could not open file "+self.path
            sys.exit()
    
    def readLine(self):
        return self.fh.readline()

    def closeLog(self):
        self.fh.close()

    def seekLogEnd(self):
        # should be 2 for versions 
        # older than 2.5 SEEK_END = 2
        self.fh.seek(0,2)
    
    def seekLogNearlyEnd(self):
        currpos = self.__getLast10Lines()
        self.fh.seek(currpos,0)
    
    def __getLast10Lines(self):
        linesep = '\n'
        self.seekLogEnd()
        charRead = ''
        currpos = self.fh.tell()
        numLines = 0
        # read one char at a time
        # as we get only last 10 lines
        # is not gonna be a lot of effort
        blockReadSize = 1
        blockCount = 1;
        self.fh.seek(-blockReadSize,2)
        while (numLines < 10):
            charRead = self.fh.read(blockReadSize)
            blockCount += 1
            if charRead == linesep:
                numLines += 1
            self.fh.seek(-blockReadSize*blockCount,2)
        # add 2, to get rid of the last seek -1 
        # and the following \n
        currpos = self.fh.tell()+2
        return currpos
        
        
    def numLines(self):
        clines = os.popen("wc -l "+self.path)
        count = clines.readline().split(" ")
        clines.close()
        nlines = int(count[0])
        #for i in self.fh:
            #count += 1
        ## go back to initial pos
        #self.fh.seek(0)
        return nlines

    def getTarget(self):
        return self.target
    
    def printa(self,line):
        if self.patarget:
            res = self.patarget.search(line)
            if res:
                print self.color.backgroundemph+line+self.color.reset
                return
        
        # tail the other lines (levels)
        if self.loglevel == "WARN":
            print self.color.warn+line+self.color.reset
        elif self.loglevel == "FATAL":
            print self.color.fatal+line+self.color.reset
        elif self.loglevel == "INFO":
            print self.color.info+line+self.color.reset
        elif self.loglevel == "ERROR":
            print self.color.error+line+self.color.reset
        elif self.loglevel == "DEBUG":
            print self.color.debug+line+self.color.reset
        else:
            print line
