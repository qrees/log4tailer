# Log4Tailer: A multicolored python tailer for log4J logs
# Copyright (C) 2008 Jordi Carrillo Bosch

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

import time

class Timer:
    """Class implementing several
    timing methods"""

    def __init__(self, end):
        self.end = end
        self.start = 0
        self.count = 0

    def startTimer(self):
        """sets the start time in epoch seconds"""
        self.start = time.time()  
                        
    def ellapsed(self):
        """return the number of seconds ellapsed"""
        now = time.time()
        ellapsed = now-self.start
        self.start = now
        return ellapsed

    def stopTimer(self):
        self.start = 0

    def timedOut(self):
        """return True if we have timed out
        False otherwise"""
        if self.ellapsed() >= self.end:
            return True
        else:
            return False

