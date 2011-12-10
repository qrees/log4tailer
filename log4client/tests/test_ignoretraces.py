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
import re
from log4tailer import notifications
from log4tailer.message import Message
from log4tailer.logcolors import LogColors
from log4tailer.logfile import Log
from log4tailer.termcolorcodes import TermColorCodes

SYSOUT = sys.stdout

class Writer:
    def __init__(self):
        self.captured = []
    
    def __len__(self):
        return len(self.captured)

    def write(self, txt):
        self.captured.append(txt)

class TestIgnoreAction(unittest.TestCase):
    def setUp(self):
        pass
    
    def testimplementsIgnore(self):
        filterRegexPat = re.compile(r'this not to be printed')
        ignoreAction = notifications.IgnoreAction(filterRegexPat)
        self.assertTrue(isinstance(ignoreAction, notifications.IgnoreAction))
        self.assertTrue(hasattr(ignoreAction, 'notify'))

    def test_ignoreline(self):
        pattern = re.compile(r'this line will not be notified')
        trace = "info hi, this line will not be notified"
        level = "INFO"
        notifier = notifications.IgnoreAction(pattern)
        sys.stdout = Writer()
        logcolors = LogColors()
        termcolors = TermColorCodes()
        message = Message(logcolors)
        anylog = Log('out.log')
        message.parse(trace, anylog)
        notifier.notify(message, anylog)
        output = logcolors.getLevelColor(level)+trace+termcolors.reset
        self.assertEqual(0, len(sys.stdout.captured))

    def test_notification(self):
        pattern = re.compile(r'this line will not be notified')
        trace = "info hi, but this line will be"
        level = "INFO"
        notifier = notifications.IgnoreAction(pattern)
        sys.stdout = Writer()
        logcolors = LogColors()
        termcolors = TermColorCodes()
        message = Message(logcolors)
        anylog = Log('out.log')
        message.parse(trace, anylog)
        notifier.notify(message, anylog)
        output = logcolors.getLevelColor(level)+trace+termcolors.reset
        self.assertEqual(output, sys.stdout.captured[0])
 
    def tearDown(self):
        sys.stdout = SYSOUT

if __name__ == '__main__':
    unittest.main()

