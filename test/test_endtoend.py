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
import time
import os
import signal
import re
import threading
import copy
sys.path.append('..')
from log4tailer.LogColors import LogColors
from log4tailer import notifications
from log4tailer.Log import Log
import log4tailer

SYSOUT = sys.stdout
LOG4TAILER_DEFAULTS = copy.deepcopy(log4tailer.defaults)

class Writer:
    def __init__(self):
        self.captured = []

    def __len__(self):
        return len(self.captured)

    def write(self, txt):
        self.captured.append(txt)

def getDefaults():
    return {'pause' : 0, 
        'silence' : False,
        'throttle' : 0,
        'actions' : [notifications.Print()],
        'nlines' : False,
        'target': None, 
        'logcolors' : LogColors(),
        'properties' : None,
        'alt_config': None}

class Interruptor(threading.Thread):
    log_name = 'out.log'
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.pid = os.getpid()

    def run(self):
        onelogtrace = 'this is an info log trace'
        anotherlogtrace = 'this is a debug log trace'
        fh = open(self.log_name, 'a')
        fh.write(onelogtrace + '\n')
        fh.write(anotherlogtrace + '\n')
        fh.close()
        time.sleep(0.02)
        os.kill(self.pid, signal.SIGINT)

class TestEndToEnd(object):
    log_name = 'onelog'

    def setUp(self):
        self.mocker = mocker.Mocker()
        self.onelog = Log(self.log_name)
        onelogtrace = 'this is an info log trace'
        anotherlogtrace = 'this is a debug log trace'
        fh = open(self.log_name, 'w')
        fh.write(onelogtrace + '\n')
        fh.write(anotherlogtrace + '\n')
        fh.close()

    class OptionsMock(object):
        def __init__(self):
            pass
        def __getattr__(self, name):
            if name == 'remote':
                return False
            elif name == 'configfile':
                return 'anythingyouwant'
            return False
   
    def test_tailerfrommonitor(self):
        sys.stdout = Writer()
        options_mock = self.OptionsMock()
        log4tailer.initialize(options_mock)
        args_mock = [self.log_name]
        interruptor = Interruptor()
        interruptor.start()
        log4tailer.monitor(options_mock, args_mock)
        interruptor.join()
        finish_trace = re.compile(r'because colors are fun')
        found = False
        for num, line in enumerate(sys.stdout.captured):
            if finish_trace.search(line):
                found = True
        if not found:
            self.fail()
    
    def tearDown(self):
        sys.stdout = SYSOUT
        log4tailer.defaults = LOG4TAILER_DEFAULTS
        if os.path.exists(self.log_name):
            os.remove(self.log_name)

if __name__ == '__main__':
    unittest.main()


