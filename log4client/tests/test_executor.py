# Log4Tailer: A multicolored python tailer for log4J logs
# Copyright (C) 2010 Jordi Carrillo Bosch

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
import mocker
from log4tailer import notifications
from log4tailer.propertyparser import Property
from log4tailer.message import Message
from log4tailer.logcolors import LogColors
from log4tailer.logfile import Log
from .utils import MemoryWriter

CONFIG = 'aconfig.txt'


# so we can run the tests in ../test or inside test
# folder
EXECUTABLE = 'python executable.py'


class PropertiesStub(object):
    def __init__(self, command, raises=False):
        self._command = command
        self._raises = raises

    def get_value(self, value):
        if self._raises:
            raise Exception("Value not found")
        return self._command


class TriggerExecutorStub(object):
    execute_msg = "executing..."

    def __init__(self, raises=False):
        self._raises = raises

    def start(self):
        pass

    def landing(self, *args):
        if self._raises:
            raise Exception
        print self.execute_msg

    def run(self):
        pass


class TestExecutor(unittest.TestCase):
    def setUp(self):
        self.mocker = mocker.Mocker()
        self.SYSOUT = sys.stdout
        sys.stdout = MemoryWriter()

    def testShouldReadExecutorFromConfigFile(self):
        command = "ls -l"
        properties = PropertiesStub(command)
        executor = notifications.Executor(properties)
        self.assertEquals(['ls', '-l'], executor.executable)

    def testShouldRaiseIfExecutorNotProvided(self):
        command = ""
        properties = PropertiesStub(command)
        self.assertRaises(Exception, notifications.Executor, properties)

    def testShouldProvideNotifyMethod(self):
        command = "ls -l"
        properties = PropertiesStub(command)
        executor = notifications.Executor(properties)
        self.assertTrue(hasattr(executor, 'notify'))

    def testFullTriggerFalseBasedOnConfig(self):
        fh = open(CONFIG, 'w')
        fh.write('executor = ls -l\n')
        fh.close()
        properties = Property(CONFIG)
        properties.parse_properties()
        executor = notifications.Executor(properties)
        self.assertEqual(False, executor.full_trigger_active)
        executor.stop()

    def testShouldNotifyWithNoFullTrigger(self):
        logcolor = LogColors()
        message = Message(logcolor)
        log = Log('anylog')
        logpath = log.path
        command = 'echo'
        properties = PropertiesStub(command)
        trace = "this is a fatal log trace"
        executor = notifications.Executor(properties,
                trigger_executor=TriggerExecutorStub)
        trigger = executor._build_trigger(trace, logpath)
        self.assertEqual(['echo'], trigger)

    def testShouldContinueIfExecutorFails(self):
        mock_proc_call = self.mocker.replace('subprocess')
        mock_proc_call.call(mocker.ANY, shell=True)
        exception_trace = "Command not found"
        self.mocker.throw(Exception(exception_trace))
        logcolor = LogColors()
        message = Message(logcolor)
        log = Log('anylog')
        trace = "this is a critical log trace"
        properties = PropertiesStub("anycommand -s")
        self.mocker.replay()
        executor = notifications.Executor(properties)
        message.parse(trace, log)
        executor.notify(message, log)
        executor.stop()
        self.assertEqual(exception_trace, sys.stdout.captured[0])

    def testShouldNotExecuteIfLevelNotInPullers(self):
        logcolor = LogColors()
        message = Message(logcolor)
        log = Log('anylog')
        command = 'anything %s %s'
        trace = "this is an info log trace"
        properties = PropertiesStub(command)
        executor = notifications.Executor(properties,
                trigger_executor=TriggerExecutorStub)
        message.parse(trace, log)
        executor.notify(message, log)
        len_captured_lines = len(sys.stdout.captured)
        self.assertEqual(len_captured_lines, 0)

    def testShouldExecuteIfTargetMessage(self):
        logcolor = LogColors()
        logfile = 'anylog'
        log = Log(logfile)
        command = "echo %s %s"
        trace = "this is an info log trace"
        trigger = ['echo', trace, logfile]
        properties = PropertiesStub(command)
        message = Message(logcolor, target='trace')
        message.parse(trace, log)
        executor = notifications.Executor(properties,
                trigger_executor=TriggerExecutorStub)
        executor.notify(message, log)
        self.assertEqual(TriggerExecutorStub.execute_msg,
                sys.stdout.captured[0])

    def tearDown(self):
        self.mocker.restore()
        self.mocker.verify()
        sys.stdout = self.SYSOUT
