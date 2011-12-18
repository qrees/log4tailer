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
from nose.tools import raises
from log4tailer.logfile import Log
from log4tailer.configuration import DefaultConfig
import log4tailer
from tests import TESTS_DIR
from os.path import join as pjoin

SYSOUT = sys.stdout
ACONFIG = 'aconfig.cfg'

class Writer(object):
    def __init__(self):
        self.captured = []

    def __len__(self):
        return len(self.captured)

    def write(self, txt):
        self.captured.append(txt)


class TestEndToEnd(unittest.TestCase):
    log_name = 'out.log'

    def setUp(self):
        self.mocker = mocker.Mocker()
        self.onelog = Log(self.log_name)
        onelogtrace = 'this is an info log trace'
        anotherlogtrace = 'this is a debug log trace'
        fh = open(self.log_name, 'w')
        fh.write(onelogtrace + '\n')
        fh.write(anotherlogtrace + '\n')
        fh.close()
        self.apicture = pjoin(TESTS_DIR, 'apicture.png')

    class _wait_for(object):

        def __init__(self, with_fatal_logtrace=False):
            self._with_fatal = with_fatal_logtrace
            self.raise_count = 0
            self.log_name = "out.log"

        def write_log(self, with_fatal_logtrace):
            fatallogtrace = 'this is a fatal log trace'
            onelogtrace = 'this is an info log trace'
            anotherlogtrace = 'this is a debug log trace'
            fh = open(self.log_name, 'a')
            if with_fatal_logtrace:
                fh.write(fatallogtrace + '\n')
            fh.write(onelogtrace + '\n')
            fh.write(anotherlogtrace + '\n')
            fh.close()

        def __call__(self, secs):
            if self.raise_count == 0:
                self.write_log(self._with_fatal)
                self.raise_count += 1
                return
            raise KeyboardInterrupt

    def test_tailerfrommonitor(self):
        sys.stdout = Writer()

        class OptionsMock(object):
            def __init__(self):
                pass
            def __getattr__(self, name):
                if name == 'remote':
                    return False
                elif name == 'configfile':
                    return 'anythingyouwant'
                return False

        options_mock = OptionsMock()
        default_config = DefaultConfig()
        log4tailer.initialize(options_mock, default_config)
        args_mock = [self.log_name]
        log4tailer.monitor(options_mock, args_mock, default_config,
                self._wait_for())
        finish_trace = re.compile(r'because colors are fun')
        found = False
        for num, line in enumerate(sys.stdout.captured):
            if finish_trace.search(line):
                found = True
        if not found:
            self.fail()

    def test_endtoend_withconfig(self):
        sys.stdout = Writer()
        fh = open(ACONFIG, 'w')
        fh.write('info = green, on_blue\n')
        fh.write('debug = yellow\n')
        fh.close()

        class OptionsMockWithConfig(object):
            def __init__(self):
                pass
            def __getattr__(self, method):
                if method == 'configfile':
                    return ACONFIG
                return False

        optionsmock_withconfig = OptionsMockWithConfig()
        default_config = DefaultConfig()
        log4tailer.initialize(optionsmock_withconfig, default_config)
        args_mock = [self.log_name]
        log4tailer.monitor(optionsmock_withconfig, args_mock, default_config,
                self._wait_for())
        finish_trace = re.compile(r'because colors are fun')
        found = False
        for num, line in enumerate(sys.stdout.captured):
            if finish_trace.search(line):
                found = True
        if not found:
            self.fail()

    def test_options_with_screenshot(self):
        sys.stdout = Writer()
        fh  = open(ACONFIG, 'w')
        fh.write('screenshot = ' + self.apicture + '\n')
        fh.close()

        class OptionWithScreenshot(object):
            def __init__(self):
                pass
            def __getattr__(self, method):
                if method == 'configfile':
                    return ACONFIG
                elif method == 'screenshot':
                    return True
                return False
        options_mock = OptionWithScreenshot()
        shot_process = pjoin(TESTS_DIR, 'printashot.sh')
        default_config = DefaultConfig()
        log4tailer.initialize(options_mock, default_config)
        default_config.actions[0].screenproc = shot_process
        args_mock = [self.log_name]
        log4tailer.monitor(options_mock, args_mock, default_config,
                self._wait_for(with_fatal_logtrace=True))
        finish_trace = re.compile(r'because colors are fun')
        found = False
        for num, line in enumerate(sys.stdout.captured):
            if finish_trace.search(line):
                found = True
        if not found:
            self.fail()
        self.assertTrue(os.path.exists(self.apicture))

    def test_printversion_andexit(self):
        sys.stdout = Writer()
        class OptionsMock(object):
            def __init__(self):
                pass
            def __getattr__(self, method):
                if method == 'version':
                    return True
                return False
        default_config = DefaultConfig()
        self.assertRaises(SystemExit, log4tailer.initialize,
                OptionsMock(), default_config)
        doc_version = re.search('\large Version (\d+\.?\d+\.?\d*)',
                open('../userguide/log4tailer.tex').read()).group(1)
        self.assertEqual(doc_version, sys.stdout.captured[0])

    def tearDown(self):
        self.mocker.restore()
        self.mocker.verify()
        sys.stdout = SYSOUT
        if os.path.exists(ACONFIG):
            os.remove(ACONFIG)
        if os.path.exists(self.log_name):
            os.remove(self.log_name)
        if os.path.exists(self.apicture):
            os.remove(self.apicture)

class TestMonitor(unittest.TestCase):
    log_name = 'out.log'

    def setUp(self):
        self.mocker = mocker.Mocker()

    @raises(SystemExit)
    def test_tailLastNlines(self):
        sys.stdout = Writer()
        fh = open(self.log_name, 'w')
        onelogtrace = 'this is an info log trace'
        anotherlogtrace = 'this is a debug log trace'
        fh.write(onelogtrace + '\n')
        fh.write(anotherlogtrace + '\n')
        fh.close()
        class OptionsMockWithNlines(object):
            def __init__(self):
                pass
            def __getattr__(self, method):
                if method == 'tailnlines':
                    return '50'
                return False
        options_mock_nlines = OptionsMockWithNlines()
        args = [self.log_name]
        default_config = DefaultConfig()
        log4tailer.initialize(options_mock_nlines, default_config)
        log4tailer.monitor(options_mock_nlines, args, default_config)

    @raises(SystemExit)
    def test_options_withremotewrongconfig(self):
        fh = open(ACONFIG, 'w')
        fh.write('anything = anything\n')
        fh.close()
        class OptionWithRemoteAndConfig(object):
            def __init__(self):
                pass
            def __getattr__(self, method):
                if method == 'configfile':
                    return ACONFIG
                elif method == 'remote':
                    return True
                return False
        options_mock = OptionWithRemoteAndConfig()
        default_config = DefaultConfig()
        log4tailer.initialize(options_mock, default_config)
        args = []
        log4tailer.monitor(options_mock, args, default_config)

    @raises(SystemExit)
    def test_options_withremotegoodconfignoconnection(self):
        getpass_mock = self.mocker.replace('getpass.getpass')
        getpass_mock()
        self.mocker.result('anypass')
        fh = open(ACONFIG, 'w')
        fh.write('sshhostnames = 127.999.9.9\n')
        fh.write('127.999.9.9 = /var/log/error.log\n')
        fh.close()
        class OptionWithRemoteAndConfig(object):
            def __init__(self):
                pass
            def __getattr__(self, method):
                if method == 'configfile':
                    return ACONFIG
                elif method == 'remote':
                    return True
                return False
        options_mock = OptionWithRemoteAndConfig()
        default_config = DefaultConfig()
        log4tailer.initialize(options_mock, default_config)
        args = []
        self.mocker.replay()
        log4tailer.monitor(options_mock, args, default_config)

    def test_options_with_poster_notification(self):
        fh = open(ACONFIG, 'w')
        fh.write('server_url = localhost\n')
        fh.write('server_port = 8000\n')
        fh.write('server_service_uri = /\n')
        fh.close()
        class OptionWithPostandConfig(object):
            def __init__(self):
                pass
            def __getattr__(self, method):
                if method == 'configfile':
                    return ACONFIG
                elif method == 'post':
                    return True
                return False
        options_mock = OptionWithPostandConfig()
        default_config = DefaultConfig()
        log4tailer.initialize(options_mock, default_config)
        self.assertTrue(default_config.post)

    def tearDown(self):
        self.mocker.restore()
        self.mocker.verify()
        sys.stdout = SYSOUT
        if os.path.exists(ACONFIG):
            os.remove(ACONFIG)
        if os.path.exists(self.log_name):
            os.remove(self.log_name)

if __name__ == '__main__':
    unittest.main()


