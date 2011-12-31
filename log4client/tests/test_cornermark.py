#!/usr/bin/env python

import unittest
import sys
import os
from log4tailer.logfile import Log
from log4tailer.message import Message
from log4tailer.logcolors import LogColors
from log4tailer import notifications
from log4tailer.termcolorcodes import TermColorCodes
from log4tailer.propertyparser import Property
from .utils import MemoryWriter


CONFIG = 'aconfig.txt'

def overgap():
    return 0.02

def tcols_callback():
    return 5

def patch_term_num_cols(notifier):
    notifier.term_num_cols = tcols_callback


class TestCornerMark(unittest.TestCase):
    """The purpose of the corner mark is to have an small square in the bottom
    right corner of the terminal to indicate something went wrong.
    """ 
    def setUp(self):
        self.sysback = sys.stdout
        self.ttcols = tcols_callback()
    
    def testIsCornerMark(self):
        cornermark = notifications.CornerMark(10)
        self.assertEquals(10, cornermark.corner_mark_time())

    def testHasNotifyMethod(self):
        cornermark = notifications.CornerMark(10)
        self.assertTrue(getattr(cornermark, 'notify'))

    def testWillMarkForSpecifiedTime(self):
        level = 'FATAL'
        trace = "FATAL there could be an error in the application"
        sys.stdout = MemoryWriter()
        logcolors = LogColors()
        termcolors = TermColorCodes()
        message = Message(logcolors)
        notifier = notifications.CornerMark(10)
        anylog = Log('out.log')
        message.parse(trace, anylog)
        patch_term_num_cols(notifier)
        padding = self.ttcols - len(notifier.MARK)
        output = padding * " " + termcolors.backgroundemph + notifier.MARK +\
                termcolors.reset
        notifier.notify(message, anylog)
        self.assertEqual(output, sys.stdout.captured[0])

    def testWillMarkforSpecifiedTimeandNotAfterwards(self):
        level = 'FATAL'
        trace = "FATAL there could be an error in the application"
        sys.stdout = MemoryWriter()
        logcolors = LogColors()
        termcolors = TermColorCodes()
        message = Message(logcolors)
        notifier = notifications.CornerMark(0.01)
        anylog = Log('out.log')
        message.parse(trace, anylog)
        padding = self.ttcols - len(notifier.MARK)
        output = padding * " " + termcolors.backgroundemph + notifier.MARK +\
                termcolors.reset
        patch_term_num_cols(notifier)
        notifier.notify(message, anylog)
        self.assertEqual(output, sys.stdout.captured[0])
        trace = "INFO this is an info trace"
        sys.stdout.flush()
        notifier.timer.corner_mark_ellapsed = overgap
        message.parse(trace, anylog)
        notifier.notify(message, anylog)
        self.assertFalse(sys.stdout.captured)

    def testNotMarkMarkedNotMark(self):
        trace = "INFO this is an info trace"
        sys.stdout = MemoryWriter()
        logcolors = LogColors()
        termcolors = TermColorCodes()
        message = Message(logcolors)
        notifier = notifications.CornerMark(0.01)
        anylog = Log('out.log')
        message.parse(trace, anylog)
        padding = self.ttcols - len(notifier.MARK)
        output = padding * " " + termcolors.backgroundemph + notifier.MARK +\
                termcolors.reset
        patch_term_num_cols(notifier)
        notifier.notify(message, anylog)
        self.assertFalse(sys.stdout.captured)
        def belowgap():
            return 0
        notifier.timer.corner_mark_ellapsed = belowgap
        level = 'FATAL'
        trace = "FATAL there could be an error in the application"
        message.parse(trace, anylog)
        notifier.notify(message, anylog)
        self.assertTrue(sys.stdout.captured)
        self.assertEquals(output, sys.stdout.captured[0])
        trace = "INFO this is an info trace"
        sys.stdout.flush()
        notifier.timer.corner_mark_ellapsed = overgap
        message.parse(trace, anylog)
        notifier.notify(message, anylog)
        self.assertFalse(sys.stdout.captured)

    def testMarkedFATALMarkedWARNING(self):
        trace = "FATAL this is a fatal trace"
        sys.stdout = MemoryWriter()
        logcolors = LogColors()
        termcolors = TermColorCodes()
        message = Message(logcolors)
        notifier = notifications.CornerMark(0.02)
        anylog = Log('out.log')
        message.parse(trace, anylog)
        notifier.notify(message, anylog)
        padding = self.ttcols - len(notifier.MARK)
        output = padding * " " + termcolors.onyellowemph + notifier.MARK +\
                termcolors.reset
        trace = "WARN this is just a warn"
        message.parse(trace, anylog)
        patch_term_num_cols(notifier)
        notifier.notify(message, anylog)
        self.assertEquals(output, sys.stdout.captured[2])

    def testMarkedTARGET(self):
        configfile = CONFIG
        logfile = "/any/path/out.log"
        trace = "this is a targeted log trace"
        fh = open(configfile, 'w')
        fh.write("targets "+logfile+"=targeted\n")
        fh.close()
        properties = Property(configfile)
        properties.parse_properties()
        sys.stdout = MemoryWriter()
        logcolors = LogColors()
        termcolors = TermColorCodes()
        notifier = notifications.CornerMark(0.02)
        anylog = Log(logfile, properties)
        message = Message(logcolors, properties = properties)
        padding = self.ttcols - len(notifier.MARK)
        output = padding * " " + termcolors.oncyanemph + notifier.MARK +\
                termcolors.reset
        message.parse(trace, anylog)
        patch_term_num_cols(notifier)
        notifier.notify(message, anylog)
        self.assertEqual(output, sys.stdout.captured[0])

    def testMarkedTARGETOverMarkableLevel(self):
        configfile = CONFIG
        logfile = "/any/path/out.log"
        trace = "this is a FATAL targeted log trace"
        fh = open(configfile, 'w')
        fh.write("targets "+logfile+"=targeted\n")
        fh.close()
        properties = Property(configfile)
        properties.parse_properties()
        sys.stdout = MemoryWriter()
        logcolors = LogColors()
        termcolors = TermColorCodes()
        notifier = notifications.CornerMark(0.02)
        anylog = Log(logfile, properties)
        message = Message(logcolors, properties = properties)
        padding = self.ttcols - len(notifier.MARK)
        output = padding * " " + termcolors.oncyanemph + notifier.MARK +\
                termcolors.reset
        message.parse(trace, anylog)
        patch_term_num_cols(notifier)
        notifier.notify(message, anylog)
        self.assertEqual(output, sys.stdout.captured[0])
    
    def tearDown(self):
        if os.path.exists(CONFIG):
            os.remove(CONFIG)
        sys.stdout = self.sysback

if __name__ == '__main__':
    unittest.main()

