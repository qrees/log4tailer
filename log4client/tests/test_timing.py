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


class TimeCounter(object):
    def __init__(self, time_value):
        self._time_value = time_value

    def __call__(self):
        return self._time_value


class TestTimer(unittest.TestCase):

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
