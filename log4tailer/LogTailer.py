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


import os, re, time, sys
import resource
from Message import Message
from LogColors import LogColors

class LogTailer:
    '''Tails the log provided by Log class'''
    def __init__(self,logcolors, pause = 1, throttleTime = 0, silence = False, action = None, fromAddress = None, toAddress = None):
        self.arrayLog = []
        self.logcolors = logcolors
        self.debug = re.compile(r'debug',re.I)
        self.info = re.compile(r'info',re.I)
        self.warn = re.compile(r'warn',re.I)
        self.error = re.compile(r'error',re.I)
        self.fatal = re.compile(r'fatal',re.I)
        self.pause = pause
        self.silence = silence
        self.action = action
        self.fromAddress = fromAddress
        self.toAddress = toAddress
        self.throttleTime = throttleTime 

    def addLog(self,log):
        self.arrayLog.append(log)
    
    def posEnd(self):
        '''Open the logs and position the cursor
        to the end'''
        for log in self.arrayLog:
            log.openLog()
            log.seekLogEnd()

    def parse(self,line):
        if (self.debug.search(line)):
            return 'DEBUG'
        elif (self.info.search(line)):
            return 'INFO'
        elif (self.warn.search(line)):
            return 'WARN'
        elif (self.error.search(line)):
            return 'ERROR'
        elif (self.fatal.search(line)):
            return 'FATAL'
        else:
            return ''
    

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
        for log in self.arrayLog:
            fd = log.openLog()
            numlines = log.numLines()
            # I could do, but would imply 
            # memory
            #numlines = len(fd.readlines())
            #fd.seek(0)
            pos = numlines-n
            count = 0
            buff = []
            ttlines = self.getTermLines()

            for curpos,line in enumerate(fd):
                if curpos >= pos:
                    line = line.rstrip()
                    loglevel = self.parse(line)
                    log.loglevel = loglevel
                    self.action.printStdOut(line,log)
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

    def tailer(self):
        '''Stdout multicolor tailer'''
        message = Message(self.logcolors)
        self.posEnd()
        if self.silence:
            self.daemonize()
        try:
            while True:
                found = 0
                # throttleTime is when our app
                # logs very fast and we want to slow
                # down the tailing
                time.sleep(self.throttleTime)
                for log in self.arrayLog:
                    if self.hasRotated(log):
                        found = 0
                    line = log.readLine()
                    if line:
                        line = line.rstrip()
                        #loglevel = self.parse(line)
                        message.parse(line)
                        self.action.triggerAction(message)
                        found = 1
                        log.size = log.getcurrSize()

                if found == 0:
                    #sleep for 1 sec
                    time.sleep(self.pause)
        except KeyboardInterrupt:
            for log in self.arrayLog:
                #print "closing "+ log.path
                log.closeLog()
            if self.silence:
                self.action.quitSMTP()
            print "Ended log4tailer, because colors are fun"
