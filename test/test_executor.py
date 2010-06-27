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
sys.path.append('..')
from log4tailer import notifications
from log4tailer.Properties import Property
from log4tailer.Message import Message
from log4tailer.LogColors import LogColors
from log4tailer.Log import Log

CONFIG = 'aconfig.txt'

class TestExecutor(unittest.TestCase):
    def setUp(self):
        self.mocker = mocker.Mocker()
    
    def testShouldReadExecutorFromConfigFile(self):
        fh = open(CONFIG, 'w')
        fh.write('executor = ls -l\n')
        fh.close()
        properties = Property(CONFIG)
        properties.parseProperties()
        executor = notifications.Executor(properties)
        self.assertEquals(['ls', '-l'], executor.executable)

    def testShouldRaiseIfExecutorNotProvided(self):
        fh = open(CONFIG, 'w')
        fh.write('anything = ls -l\n')
        fh.close()
        properties = Property(CONFIG)
        properties.parseProperties()
        self.assertRaises(Exception, notifications.Executor, properties)

    def testShouldProvideNotifyMethod(self):
        fh = open(CONFIG, 'w')
        fh.write('executor = ls -l\n')
        fh.close()
        properties = Property(CONFIG)
        properties.parseProperties()
        executor = notifications.Executor(properties)
        self.assertTrue(hasattr(executor, 'notify'))

    def testFullTriggerTrueTwoPlaceHoldersBasedOnConfig(self):
        fh = open(CONFIG, 'w')
        fh.write('executor = ls -l %s %s\n')
        fh.close()
        properties = Property(CONFIG)
        properties.parseProperties()
        executor = notifications.Executor(properties)
        self.assertEqual(True, executor.full_trigger_active)

    def testFullTriggerFalseBasedOnConfig(self):
        fh = open(CONFIG, 'w')
        fh.write('executor = ls -l\n')
        fh.close()
        properties = Property(CONFIG)
        properties.parseProperties()
        executor = notifications.Executor(properties)
        self.assertEqual(False, executor.full_trigger_active)

    def testShouldNotifyWithFullTrigger(self):
        logcolor = LogColors()
        message = Message(logcolor)
        log = Log('anylog')
        fh = open(CONFIG, 'w')
        fh.write('executor = ls -l %s %s\n')
        fh.close()
        trigger = "ls -l this is a log trace anylog"
        trace = "this is a log trace"
        properties = Property(CONFIG)
        properties.parseProperties()
        executor = notifications.Executor(properties)
        os_mock = self.mocker.replace('os')
        os_mock.system(trigger)
        self.mocker.result(True)
        self.mocker.replay()
        message.parse(trace, log)
        executor.notify(message, log)
    
    def testShouldNotifyWithNoFullTrigger(self):
        logcolor = LogColors()
        message = Message(logcolor)
        log = Log('anylog')
        fh = open(CONFIG, 'w')
        fh.write('executor = echo\n')
        fh.close()
        trace = "this is a log trace"
        properties = Property(CONFIG)
        properties.parseProperties()
        executor = notifications.Executor(properties)
        message.parse(trace, log)
        executor.notify(message, log)

    def testShouldNotifyAndContinueIfExecutorFails(self):
        logcolor = LogColors()
        message = Message(logcolor)
        log = Log('anylog')
        fh = open(CONFIG, 'w')
        fh.write('executor = anycommand\n')
        fh.close()
        trace = "this is a log trace"
        properties = Property(CONFIG)
        properties.parseProperties()
        executor = notifications.Executor(properties)
        message.parse(trace, log)
        executor.notify(message, log)
        
    def tearDown(self):
        self.mocker.restore()
        self.mocker.verify()

if __name__ == '__main__':
    unittest.main()

