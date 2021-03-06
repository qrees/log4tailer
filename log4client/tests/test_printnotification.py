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
from log4tailer.strategy import TailContext
from log4tailer.strategy import TailOneLineMethod
from log4tailer.strategy import TailMultiLineMethod
from log4tailer.message import Message
from log4tailer.logcolors import LogColors
from log4tailer import notifications
from log4tailer.termcolorcodes import TermColorCodes
import socket
from .utils import MemoryWriter

SYSOUT = sys.stdout


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


class PropertiesTraceStub(object):

    def __init__(self):
        pass

    def get_value(self, key):
        if key == 'tracespacing':
            return 1
        if key == 'slowdown':
            # would slow down for 5 seconds
            # one log trace/second
            return 5
        return "false"


class MessageMock(object):
    def __init__(self, logtrace):
        self.logtrace = logtrace

    def getColorizedMessage(self):
        return (0, self.logtrace)


class LogMock(object):
    def __init__(self):
        pass


class TestPrintWithHostname(unittest.TestCase):

    def setUp(self):
        self.sysout = sys.stdout

    def test_hostnameinconfig(self):
        logfile = 'out.log'
        fh = open(logfile, 'w')
        someLogTraces = ['FATAL> something went wrong',
                              'ERROR> not so wrong',
                              'WARN> be careful',
                              'DEBUG> looking behind the scenes',
                              'INFO> the app is running']
        for line in someLogTraces:
            fh.write(line + '\n')
        fh.close()
        logcolors = LogColors()  # using default colors
        termcolors = TermColorCodes()
        target = None
        notifier = notifications.Print(PropertiesMock())
        message = Message(logcolors, target)
        log = Log(logfile)
        log.openLog()
        sys.stdout = MemoryWriter()
        hostname = socket.gethostname()
        for _ in range(len(someLogTraces)):
            line = log.readLine()
            line = line.rstrip()
            level = line.split('>')
            message.parse(line, log)
            output = (hostname + ': ' +
                    logcolors.getLevelColor(level[0]) +
                    line +
                    termcolors.reset)
            notifier.notify(message, log)
            self.assertTrue(output in sys.stdout.captured)
        line = log.readLine()
        self.assertEqual('', line)
        message.parse(line, log)
        self.assertFalse(notifier.notify(message, log))

    def tearDown(self):
        sys.stdout = self.sysout


class PrintTraceSpacing(unittest.TestCase):

    def setUp(self):
        self.sysout = sys.stdout

    def test_oneline_space_between_traces(self):
        sys.stdout = MemoryWriter()
        notifier = notifications.Print(PropertiesTraceStub())
        logtrace = "this is a log trace in red"
        message = MessageMock(logtrace)
        log = LogMock()
        notifier.notify(message, log)
        expected_logtrace = "\n" + logtrace
        self.assertEqual(expected_logtrace, sys.stdout.captured[0])

    def tearDown(self):
        sys.stdout = self.sysout


class WaitForMock(object):

    def __init__(self):
        self.called = False

    def __call__(self):
        self.called = True


class TailMethod(object):
    def __init__(self):
        pass

    def get_trace(self, log):
        return "hi"


class OtherTailMethod(object):
    """docstring for OtherTailMethod"""
    def __init__(self):
        pass


class TailContextTestCase(unittest.TestCase):

    def test_instantiates(self):
        throttle_time = 0
        context = TailContext(throttle_time, default_tail_method=TailMethod)
        self.assertTrue(isinstance(context, TailContext))

    def test_changes_tail_method(self):
        throttle_time = 0
        context = TailContext(throttle_time, default_tail_method=TailMethod)
        context.change_tail_method(OtherTailMethod())
        self.assertTrue(isinstance(context.tail_method, OtherTailMethod))

    def test_get_trace(self):
        throttle_time = 0
        context = TailContext(throttle_time, default_tail_method=TailMethod)
        trace = context.get_trace(DummyLog())
        self.assertEqual(trace, "hi")


class DummyLog(object):
    def __init__(self):
        pass

    def readLine(self):
        return "one line"

    def readLines(self):
        return "many lines"


class TailOneLineMethodTestCase(unittest.TestCase):

    def test_instantiates(self):
        one_line_method = TailOneLineMethod()
        self.assertTrue(isinstance(one_line_method, TailOneLineMethod))

    def test_get_trace(self):
        one_line_method = TailOneLineMethod()
        self.assertTrue(one_line_method.read_method, "readLine")
        trace = one_line_method.get_trace(DummyLog())
        self.assertEqual(trace, "one line")


class TailMultiLineMethodTestCase(unittest.TestCase):

    def test_instantiates(self):
        one_line_method = TailMultiLineMethod()
        self.assertTrue(isinstance(one_line_method, TailMultiLineMethod))

    def test_get_trace(self):
        one_line_method = TailMultiLineMethod()
        self.assertTrue(one_line_method.read_method, "readLines")
        trace = one_line_method.get_trace(DummyLog())
        self.assertEqual(trace, "many lines")


class WarningMessage(object):
    def __init__(self):
        self.messageLevel = "warn"

    def isATarget(self):
        return False


class NormalMessage(object):
    def __init__(self):
        self.messageLevel = "info"

    def isATarget(self):
        return False


class SlowDownNotificationTestCase(unittest.TestCase):

    def test_instantiates(self):
        throttle_time = 0
        context = TailContext(throttle_time)
        slow_down = notifications.SlowDown(context)
        self.assertTrue(isinstance(slow_down, notifications.SlowDown))

    def test_notify_changes_tail_method(self):
        throttle_time = 0
        context = TailContext(throttle_time)
        self.assertTrue(isinstance(context.tail_method, TailMultiLineMethod))
        slow_down = notifications.SlowDown(context)
        slow_down.notify(WarningMessage(), DummyLog())
        self.assertTrue(isinstance(context.tail_method, TailOneLineMethod))

    def test_notify_back_to_default_after_1_tails(self):
        throttle_time = 0
        context = TailContext(throttle_time)
        self.assertTrue(isinstance(context.tail_method, TailMultiLineMethod))
        slow_down = notifications.SlowDown(context)
        notifications.SlowDown.MAX_COUNT = 1
        slow_down.notify(WarningMessage(), DummyLog())
        self.assertTrue(isinstance(context.tail_method, TailOneLineMethod))
        slow_down.notify(NormalMessage(), DummyLog())
        slow_down.notify(NormalMessage(), DummyLog())
        self.assertTrue(isinstance(context.tail_method, TailMultiLineMethod))

    def test_notify_no_change_context(self):
        throttle_time = 0
        context = TailContext(throttle_time)
        self.assertTrue(isinstance(context.tail_method, TailMultiLineMethod))
        slow_down = notifications.SlowDown(context)
        slow_down.notify(NormalMessage(), DummyLog())
        self.assertFalse(slow_down.triggered)
