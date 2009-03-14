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


import re

class ColorParser:
    def __init__(self):
        
        self.debug = re.compile(r'debug',re.I)
        self.info = re.compile(r'info',re.I)
        self.warn = re.compile(r'warn',re.I)
        self.error = re.compile(r'error',re.I)
        self.fatal = re.compile(r'fatal',re.I)
        
    def parse(self,line):
        if (self.debug.search(line)):
            return 'DEBUG'
        elif (self.info.search(line)):
            return 'INFO'
        elif (self.warn.search(line)):
            return 'WARN'
        elif (self.error.search(line)):
            return 'ERROR'
        elif (self.fatal.search(line)):
            return 'FATAL'
        else:
            return ''
