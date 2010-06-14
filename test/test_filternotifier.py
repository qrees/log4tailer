#!/usr/bin/env python

import unittest
import sys
import os
import re
from os.path import dirname, abspath, join as pjoin
sys.path.append(pjoin(abspath(dirname(__file__)), os.pardir))
from log4tailer import notifications
from log4tailer.Message import Message
from log4tailer.LogColors import LogColors
from log4tailer.Log import Log
from log4tailer.TermColorCodes import TermColorCodes

SYSOUT = sys.stdout

class Writer:
    def __init__(self):
        self.captured = []
    
    def __len__(self):
        return len(self.captured)

    def write(self, txt):
        self.captured.append(txt)

class TestFilterNotifier(unittest.TestCase):
    def setUp(self):
        pass
    
    def testimplementsFilter(self):
        filterRegexPat = re.compile(r'this not to be printed')
        filterNotifier = notifications.Filter(filterRegexPat)
        self.assertTrue(isinstance(filterNotifier, notifications.Filter))
        self.assertTrue(hasattr(filterNotifier, 'notify'))

    def testnotify(self):
        pattern = re.compile(r'hi, this line to be notified')
        trace = "info hi, this line to be notified"
        level = "INFO"
        notifier = notifications.Filter(pattern)
        sys.stdout = Writer()
        logcolors = LogColors()
        termcolors = TermColorCodes()
        message = Message(logcolors)
        anylog = Log('out.log')
        message.parse(trace, anylog)
        notifier.notify(message, anylog)
        output = logcolors.getLevelColor(level)+trace+termcolors.reset
        self.assertEqual(output, sys.stdout.captured[0])

    def testnoNotification(self):
        pattern = re.compile(r'hi, this line to be notified')
        trace = "info this is just a log trace"
        notifier = notifications.Filter(pattern)
        sys.stdout = Writer()
        logcolors = LogColors()
        message = Message(logcolors)
        anylog = Log('out.log')
        message.parse(trace, anylog)
        notifier.notify(message, anylog)
        # assert is empty
        self.assertFalse(sys.stdout.captured)

    def tearDown(self):
        sys.stdout = SYSOUT

if __name__ == '__main__':
    unittest.main()

