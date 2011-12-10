# Log4Tailer: A multicolored python tailer for log4J logs
# Copyright (C) 2011 Jordi Carrillo Bosch

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
import sys
from log4tailer.logfile import Log
from log4tailer.message import Message
from log4tailer.LogColors import LogColors
from log4tailer import notifications
from log4tailer.TermColorCodes import TermColorCodes
import socket

SYSOUT = sys.stdout

class Writer:
    def __init__(self):
        self.captured = []
    
    def __len__(self):
        return len(self.captured)

    def write(self, txt):
        self.captured.append(txt)

class PropertiesMock(object):
    """docstring for Properties"""
    def __init__(self):
        pass

    def get_keys(self):
        return ['print_hostname']

    def get_value(self, key):
        if key == 'print_hostname':
            return "true"

    def is_key(self, key):
        return True


class TestPrintWithHostname(unittest.TestCase):
    def setUp(self):
        self.logfile = 'out.log'
        fh = open(self.logfile,'w')
        self.someLogTraces = ['FATAL> something went wrong',
                              'ERROR> not so wrong',
                              'WARN> be careful',
                              'DEBUG> looking behind the scenes',
                              'INFO> the app is running']
        for line in self.someLogTraces:
            fh.write(line+'\n')
        fh.close()
        self.sysout = sys.stdout

    def test_hostnameinconfig(self):
        logcolors = LogColors() #using default colors
        termcolors = TermColorCodes()
        target = None
        notifier = notifications.Print(PropertiesMock())
        message = Message(logcolors,target)
        log = Log(self.logfile)
        log.openLog()
        sys.stdout = Writer()
        hostname = socket.gethostname()
        for count in range(len(self.someLogTraces)):
            line = log.readLine()
            line = line.rstrip()
            level = line.split('>')
            message.parse(line, log)
            output = (hostname + ': ' +
                    logcolors.getLevelColor(level[0]) +
                    line +
                    termcolors.reset)
            notifier.notify(message,log)
            self.assertTrue(output in sys.stdout.captured)
        line = log.readLine()
        self.assertEqual('',line)
        message.parse(line, log)
        self.assertFalse(notifier.notify(message,log))

    def tearDown(self):
        sys.stdout = self.sysout
    
 
