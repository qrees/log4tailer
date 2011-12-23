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

class Timer(object):
    """Class implementing several
    timing methods"""

    def __init__(self, notify_thr=60, time_counter=time.time):
        self._start = 0
        self.count = 0
        self._notify_thr = notify_thr
        self._time_counter = time_counter

    def _now(self):
        return self._time_counter()

    def startTimer(self):
        """sets the start time in epoch seconds"""
        self._start = self._now()
        return self._start
    
    def ellapsed(self):
        return self._now() - self._start

    def _update_timer(self):
        """return the number of seconds ellapsed"""
        # the count is to avoid not sending
        # an alert when is the first time you call
        # ellapsed and is below the gap notification time
        self._start = self._now()
        return self._start

    def corner_mark_ellapsed(self):
        return self.ellapsed()

    def inactivityEllapsed(self):
        return self.ellapsed()

    def stopTimer(self):
        self._start = 0
        return self._start

    def over_threshold(self, ellapsed):
        return ellapsed > self._notify_thr

    def in_safeguard_gap(self):
        if self.over_threshold(self.inactivityEllapsed()):
            self.reset()
            return False
        return True

    def awaitSend(self, triggeredNotSent):
        """return True if we have timed out
        False otherwise"""
        # triggered not sent; when it was
        # triggered but we are in an awaiting
        # gap period
        if triggeredNotSent:
            return self.in_safeguard_gap()
        self.reset()
        ellapsed = self.ellapsed()
        if self.ellapsed <= self._notify_thr and self.count == 0:
            self.count += 1
            return False
        elif self.over_threshold(self.ellapsed()):
            return False
        return True

    def reset(self):
        return self._update_timer()

