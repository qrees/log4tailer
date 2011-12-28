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
from log4tailer import setup_config
from log4tailer import notifications
from log4tailer.configuration import DefaultConfig
from .utils import MemoryWriter
from hamcrest import assert_that, contains_string
import sys
import log4tailer
import mocker


class OptionsMock(object):

    def __init__(self, to_mock):
        self._to_mock = to_mock

    @property
    def filter(self):
        return "anyregex"

    @property
    def ignore(self):
        return "anyregex"

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


class OptionsWithNLines(object):
    def __init__(self):
        pass

    def __getattr__(self, method):
        return False

    @property
    def tailnlines(self):
        return "56700"


class TestInitialize(unittest.TestCase):
    def setUp(self):
        sysoutback = sys.stdout
        sys.stdout = MemoryWriter()
        self.mocker = mocker.Mocker()

    def test_shoutsversion_andexits(self):
        log4tailer.__version__ = "3.0"
        self.assertRaises(SystemExit, setup_config, OptionsMock("version"),
            DefaultConfig())
        assert_that(sys.stdout.captured[0], contains_string("3.0"))

    def test_has_pauseoption_setup(self):
        config = DefaultConfig()
        setup_config(OptionsMock("blablabla"), config)
        self.assertEqual(4500, config.pause)

    def test_has_throttle_setup(self):
        config = DefaultConfig()
        setup_config(OptionsWithThrottle(), config)
        self.assertEqual(0.05, config.throttle)

    def test_nomailsilence_setup(self):
        config = DefaultConfig()
        setup_config(OptionsMock("nomailsilence"), config)
        self.assertTrue(config.silence)

    def test_mail_properties_setup(self):
        config = DefaultConfig()

        def callback():
            return False

        class MyProperties(object):
            def __init__(self):
                pass

            def get_value(self, value):
                return callback

            def __getattr__(self, method):
                return False

        config.properties = MyProperties()
        setup_mail_mock = self.mocker.replace('log4tailer.setup_mail')
        setup_mail_mock(mocker.ANY)

        class MyAction(object):
            def __init__(self):
                pass

        self.mocker.result(MyAction())
        self.mocker.replay()
        setup_config(OptionsMock("mail"), config)
        last_action = config.actions[-1:][0]
        self.assertTrue(isinstance(last_action, MyAction))

    def test_filternotification_setup(self):
        """Filter notification overrides print notification, which is the
        default notification in the actions array.
        """
        config = DefaultConfig()
        setup_config(OptionsMock("blablabla"), config)
        self.assertTrue(isinstance(config.actions[0], notifications.Filter))

    def test_ignorenotification_setup(self):
        config = DefaultConfig()
        setup_config(OptionsMock("blablabla"), config)
        self.assertTrue(isinstance(config.actions[0],
            notifications.IgnoreAction))

    def test_lastnlines(self):
        config = DefaultConfig()
        setup_config(OptionsWithNLines(), config)
        self.assertEqual(config.nlines, 56700)

    def test_target_setup(self):
        config = DefaultConfig()
        setup_config(OptionsMock("target"), config)
        self.assertTrue(config.target)

    def test_cornermark_setup(self):
        config = DefaultConfig()
        setup_config(OptionsMock("cornermark"), config)
        last_action = config.actions[-1:][0]
        self.assertTrue(isinstance(last_action, notifications.CornerMark))

    def tearDown(self):
        self.mocker.restore()
        self.mocker.verify()
