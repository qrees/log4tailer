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
import os
from log4tailer.logfile import Log
from log4tailer.configuration import DefaultConfig
import log4tailer
from hamcrest import assert_that
from hamcrest import is_in

SYSOUT = sys.stdout
SYSIN = sys.stdin
SYSERR = sys.stderr
ACONFIG = 'aconfig.cfg'


class Writer:
    def __init__(self):
        self.captured = []

    def __len__(self):
        return len(self.captured)

    def write(self, txt):
        self.captured.append(txt)

    def fileno(self):
        return True

    def flush(self):
        pass


class Reader(object):
    """docstring for Reader"""
    def __init__(self):
        pass

    def fileno(self):
        return True

    def __getattr__(self, method):
        pass


class TestDemon(unittest.TestCase):
    log_name = 'out.log'

    def setUp(self):
        self.utils_back = log4tailer.setup_mail
        self.os_fork = os.fork
        self.os_chdir = os.chdir
        self.os_umask = os.umask
        self.os_dup2 = os.dup2
        self.os_setsid = os.setsid
        self.onelog = Log(self.log_name)
        onelogtrace = 'this is an info log trace'
        anotherlogtrace = 'this is a debug log trace'
        fh = open(self.log_name, 'w')
        fh.write(onelogtrace + '\n')
        fh.write(anotherlogtrace + '\n')
        fh.close()
        self.raise_count = 0

    def test_demonizedoptionsilence(self):
        sys.stdout = Writer()
        sys.stderr = Writer()
        sys.stdin = Reader()
        fh = open(ACONFIG, 'w')
        fh.write('info = green, on_blue\n')
        fh.write('debug = yellow\n')
        fh.close()

        class OptionsMock2(object):
            def __init__(self):
                pass

            def __getattr__(self, method):
                if method == 'silence':
                    return True
                if method == 'configfile':
                    return ACONFIG
                return False

        class ActionMock(object):
            def __init__(self):
                pass

            def notify(self, message, log):
                pass

        def setup_mail(properties):
            return ActionMock()

        def wait_for(secs):
            if self.raise_count == 0:
                write_log()
                return
            raise KeyboardInterrupt

        def chdir(directory):
            return True

        def umask(integer):
            return True

        def setsid():
            return True

        def dup2(one, two):
            return True

        def fork():
            return -1

        onelogtrace = 'this is an info booo log trace'
        anotherlogtrace = 'this is a debug log trace'

        def write_log():
            fh = open(self.log_name, 'a')
            fh.write(onelogtrace + '\n')
            fh.write(anotherlogtrace + '\n')
            fh.close()
            self.raise_count += 1

        log4tailer.setup_mail = setup_mail
        options_mock = OptionsMock2()
        args = [self.log_name]
        default_config = DefaultConfig()
        log4tailer.initialize(options_mock, default_config)
        os.fork = fork
        os.chdir = chdir
        os.setsid = setsid
        os.dup2 = dup2
        os.umask = umask
        log4tailer.monitor(options_mock, args, default_config,
                wait_for)
        expectedlogtrace = ("\x1b[32m\x1b[44mthis is an info booo log "
            "trace\x1b[0m")
        assert_that(expectedlogtrace,
                is_in(sys.stdout.captured))

    def tearDown(self):
        sys.stdout = SYSOUT
        sys.stdin = SYSIN
        sys.stderr = SYSERR
        os.fork = self.os_fork
        os.setsid = self.os_setsid
        os.chdir = self.os_chdir
        os.umask = self.os_umask
        os.dup2 = self.os_dup2
        log4tailer.setup_mail = self.utils_back
        if os.path.exists(self.log_name):
            os.remove(self.log_name)
        if os.path.exists(ACONFIG):
            os.remove(ACONFIG)
