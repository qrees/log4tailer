#!/usr/bin/env python

import unittest
import sys
from log4tailer.logfile import Log
from log4tailer.message import Message
from log4tailer.logcolors import LogColors
from log4tailer import notifications
from log4tailer.termcolorcodes import TermColorCodes
from .utils import MemoryWriter
from mock import patch


class PropertiesStub(object):
    def __init__(self):
        pass

    def get_value(self, value):
        return "targeted"


def overgap():
    return 0.02


def tcols_callback():
    return 5


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

    @patch('log4tailer.notifications.term_num_cols', tcols_callback)
    def testWillMarkForSpecifiedTime(self):
        trace = "FATAL there could be an error in the application"
        sys.stdout = MemoryWriter()
        logcolors = LogColors()
        termcolors = TermColorCodes()
        message = Message(logcolors)
        notifier = notifications.CornerMark(10)
        anylog = Log('out.log')
        message.parse(trace, anylog)
        padding = self.ttcols - len(notifier.MARK)
        output = padding * " " + termcolors.backgroundemph + notifier.MARK +\
                termcolors.reset
        notifier.notify(message, anylog)
        self.assertEqual(output, sys.stdout.captured[0])

    @patch('log4tailer.notifications.term_num_cols', tcols_callback)
    def testWillMarkforSpecifiedTimeandNotAfterwards(self):
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
        notifier.notify(message, anylog)
        self.assertEqual(output, sys.stdout.captured[0])
        trace = "INFO this is an info trace"
        sys.stdout.flush()
        notifier.timer.corner_mark_ellapsed = overgap
        message.parse(trace, anylog)
        notifier.notify(message, anylog)
        self.assertFalse(sys.stdout.captured)

    @patch('log4tailer.notifications.term_num_cols', tcols_callback)
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
        notifier.notify(message, anylog)
        self.assertFalse(sys.stdout.captured)

        def belowgap():
            return 0

        notifier.timer.corner_mark_ellapsed = belowgap
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

    @patch('log4tailer.notifications.term_num_cols', tcols_callback)
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
        notifier.notify(message, anylog)
        self.assertEquals(output, sys.stdout.captured[2])

    @patch('log4tailer.notifications.term_num_cols', tcols_callback)
    def testMarkedTARGET(self):
        logfile = "/any/path/out.log"
        trace = "this is a targeted log trace"
        sys.stdout = MemoryWriter()
        logcolors = LogColors()
        termcolors = TermColorCodes()
        notifier = notifications.CornerMark(0.02)
        anylog = Log(logfile, PropertiesStub())
        message = Message(logcolors, properties=PropertiesStub())
        padding = self.ttcols - len(notifier.MARK)
        output = padding * " " + termcolors.oncyanemph + notifier.MARK +\
                termcolors.reset
        message.parse(trace, anylog)
        notifier.notify(message, anylog)
        self.assertEqual(output, sys.stdout.captured[0])

    @patch('log4tailer.notifications.term_num_cols', tcols_callback)
    def testMarkedTARGETOverMarkableLevel(self):
        logfile = "/any/path/out.log"
        trace = "this is a FATAL targeted log trace"
        sys.stdout = MemoryWriter()
        logcolors = LogColors()
        termcolors = TermColorCodes()
        notifier = notifications.CornerMark(0.02)
        anylog = Log(logfile, PropertiesStub())
        message = Message(logcolors, properties=PropertiesStub)
        padding = self.ttcols - len(notifier.MARK)
        output = padding * " " + termcolors.oncyanemph + notifier.MARK +\
                termcolors.reset
        message.parse(trace, anylog)
        notifier.notify(message, anylog)
        self.assertEqual(output, sys.stdout.captured[0])

    def tearDown(self):
        sys.stdout = self.sysback
