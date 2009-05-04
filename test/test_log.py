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


import unittest
import os,sys

sys.path.append('..')
from log4tailer.Log import Log

class TestLog(unittest.TestCase):

    def setUp(self):
        '''creates a log file
        and opens it to make some tests'''
        self.logfile = open('out.log','w')
        self.aline = "this is a line in the log\n"
        self.logfile.write(self.aline)
        self.logfile.close()
        self.logname = 'out.log'
    
    def openLog(self):
        log = Log(self.logname)
        log.openLog()
        return log 

    def writeNlines(self,nlines):
        logfile = open(self.logname,'a')
        for count in range(nlines):
            logfile.write(self.aline)
        logfile.close()

    def testLogCanRead(self):
        log = self.openLog()
        self.assertEqual(self.aline,log.readLine())

    def testLogHasRotated(self):
        log = self.openLog()
        self.tearDown()
        self.setUp()
        self.assertNotEqual(log.inode,log.getcurrInode)
    
    def testLogSeekEnd(self):
        log = self.openLog()
        log.seekLogEnd()
        # we should be at the end
        self.assertEqual('',log.readLine())
        log.closeLog()

    def testLogNearlyEnd(self):
        log = self.openLog()
        log.seekLogNearlyEnd()
        # log has been positioned 
        # to read the last 10 lines
        # by now. As we have only one line in the log
        # make sure is the only one we read
        # and is the same as the one in there
        self.assertEqual(self.aline,log.readLine())
        log.closeLog()
        # test we read exactly last 10 lines
        self.writeNlines(20)
        log = self.openLog()
        log.seekLogNearlyEnd()
        # read till the end
        count = 0
        while log.readLine():
            count += 1
        self.assertEqual(10,count)

    def tearDown(self):
        os.remove(self.logname)

if __name__ == '__main__':
        unittest.main()
        

