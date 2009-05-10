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


class Resume():

    def __init__(self):
        self.levels = {'DEBUG':0,
                       'INFO':0,
                       'WARN':0,
                       'ERROR':0,
                       'FATAL':0}

    def update(self,messageLevel):
        if self.levels.has_key(messageLevel):
            self.levels[messageLevel] += 1

    def getInfo(self,messageLevel):
        return self.levels[messageLevel]

    def spit(self):
        print "Analytics: "
        for key,val in self.levels.iteritems():
            print "level "+key+": "+str(val)

                       
