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
from log4tailer.timing import Timer
import mocker


class TimeCounter(object):
    def __init__(self, time_value):
        self._time_value = time_value

    def __call__(self):
        return self._time_value


class TestTimer(unittest.TestCase):

    def setUp(self):
        self.mocker = mocker.Mocker()

    def test_instantiates(self):
        timer = Timer()
        self.assertTrue(isinstance(timer, Timer))

    def test_instantiates_with_threshold(self):
        timer = Timer(notify_thr=120)
        self.assertTrue(isinstance(timer, Timer))

    def test_start_timer(self):
        timer = Timer(time_counter=TimeCounter(10))
        self.assertEqual(timer.startTimer(), 10)

    def test_stop_timer(self):
        timer = Timer(time_counter=TimeCounter(10))
        self.assertEqual(timer.stopTimer(), 0)

    def test_ellapsed(self):
        timer = Timer(time_counter=TimeCounter(0))
        self.assertEqual(timer.ellapsed(), 0)

    def test_ellapsed_with_start(self):
        timer = Timer(time_counter=TimeCounter(5))
        timer.startTimer()
        self.assertEqual(timer.ellapsed(), 0)

    def test_over_threshold(self):
        timer = Timer(notify_thr=1)
        self.assertTrue(timer.over_threshold(3))

    def test_below_threshold(self):
        timer = Timer(notify_thr=2)
        self.assertFalse(timer.over_threshold(1))

    def test_reset(self):
        timer = Timer(time_counter=TimeCounter(5))
        self.assertEqual(timer.reset(), 5)

    def test_no_await_sending(self):
        timer = Timer(time_counter=TimeCounter(5))
        timer_proxy = self.mocker.proxy(timer)
        timer_proxy.over_threshold(mocker.ANY)
        self.mocker.result(True)
        self.mocker.replay()
        # do not await sending. We are over gap 
        self.assertFalse(timer.in_safeguard_gap.im_func(timer_proxy))

    def test_await_sending(self):
        timer = Timer(time_counter=TimeCounter(5))
        timer_proxy = self.mocker.proxy(timer)
        timer_proxy.over_threshold(mocker.ANY)
        self.mocker.result(False)
        self.mocker.replay()
        # await sending. We are still in the safe guard gap
        self.assertTrue(timer.in_safeguard_gap.im_func(timer_proxy))

    def tearDown(self):
        self.mocker.restore()
        self.mocker.verify()

