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


class PropertiesTraceSpacing(object):

    def __init__(self):
        pass

    def get_value(self, key):
        if key == 'tracespacing':
            return 1
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
        notifier = notifications.Print(PropertiesTraceSpacing())
        logtrace = "this is a log trace in red"
        message = MessageMock(logtrace)
        log = LogMock()
        notifier.notify(message, log)
        expected_logtrace = "\n" + logtrace
        self.assertEqual(expected_logtrace, sys.stdout.captured[0])

    def tearDown(self):
        sys.stdout = self.sysout
