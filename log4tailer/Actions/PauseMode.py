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


class PauseMode:
    '''In PrintAction if an specific
    level is found, it will pause so we will
    not miss a level'''

    def __init__(self):
        self.defaultLevelPauses = {'DEBUG':0,'INFO':0, 'WARN':1, 'ERROR':3, 'FATAL':5, 'TARGET':5}

    def getPause(self,level):
        return self.defaultLevelPauses[level]

    def parseConfig(self,properties):
        pauseKeys = ['pauseDEBUG','pauseINFO','pauseWARN','pauseERROR','pauseFATAL','pauseTARGET']
        for pauseKey in pauseKeys:
            try:
                level = pauseKey.split('pause')[1]
                pauseLevel = float(properties.getValue(pauseKey))
                self.defaultLevelPauses[level] = pauseLevel
            except:
                pass
