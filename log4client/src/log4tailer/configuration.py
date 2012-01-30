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


import os
from . import logcolors
from . import strategy

class DefaultConfig(object):
    def __init__(self):
        self.actions = []
        self.pause = 1
        self.silence = False
        self.throttle = 0
        self.nlines = False
        self.target = None
        self.logcolors = logcolors.LogColors()
        self.properties = None
        self.alt_config = os.path.expanduser('~/.log4tailer')
        self.post = False
        self.tail_context = strategy.TailContext(self.throttle)
