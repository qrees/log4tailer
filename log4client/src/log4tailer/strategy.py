#!/usr/bin/env python

# Log4Tailer: A multicolored python tailer for log4J logs
# Copyright (C) 2012 Jordi Carrillo Bosch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


class TailOneLineMethod(object):
    def __init__(self):
        self.read_method = "readLine"

    def get_trace(self, log):
        return getattr(log, self.read_method)()


class TailMultiLineMethod(object):

    def __init__(self):
        self.read_method = "readLines"

    def get_trace(self, log):
        return getattr(log, self.read_method)()


class TailContext(object):

    def __init__(self, throttle_time, default_tail_method=TailMultiLineMethod):
        self.tail_method = default_tail_method()
        self.throttle_time = throttle_time

    def change_tail_method(self, tail_method):
        self.tail_method = tail_method

    def get_trace(self, log):
        return self.tail_method.get_trace(log)
