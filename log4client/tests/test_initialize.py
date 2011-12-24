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
from log4tailer import initialize
from log4tailer.configuration import DefaultConfig
from .utils import MemoryWriter
from hamcrest import assert_that, contains_string
import sys
import log4tailer
import mocker


class OptionsMock(object):

    def __init__(self, to_mock):
        self._to_mock = to_mock

    def __getattr__(self, method):
        if self._to_mock == method:
            return True
        return False
    
    @property
    def pause(self):
        return "4500"


class OptionsWithThrottle(object):

    def __init__(self):
        pass
    
    def __getattr__(self, method):
        return False

    @property
    def throttle(self):
        return "0.05"


class TestInitialize(unittest.TestCase):
    def setUp(self):
        sysoutback = sys.stdout
        sys.stdout = MemoryWriter()
        self.mocker = mocker.Mocker()

    def test_shoutsversion_andexits(self):
        log4tailer.__version__ = "3.0"
        self.assertRaises(SystemExit, initialize, OptionsMock("version"),
            DefaultConfig())
        assert_that(sys.stdout.captured[0], contains_string("3.0"))

    def test_has_pauseoption_setup(self):
        config = DefaultConfig()
        initialize(OptionsMock("blablabla"), config)
        self.assertEqual(4500, config.pause)

    def test_has_throttle_setup(self):
        config = DefaultConfig()
        initialize(OptionsWithThrottle(), config)
        self.assertEqual(0.05, config.throttle)

    def tearDown(self):
        self.mocker.restore()
        self.mocker.verify()
