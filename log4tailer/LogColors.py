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


from Properties import Property
from TermColorCodes import TermColorCodes

class LogColors:
    '''Provides the colors that will
    be used when printing Log4J levels'''
    def __init__(self):
        self.color = TermColorCodes()
        # defaults
        self.warn = self.color.yellow
        self.error = self.color.magenta
        self.info = self.color.green
        self.debug = self.color.black
        self.fatal = self.color.red
        self.reset = self.color.reset
        self.backgroundemph = self.color.backgroundemph

    def parseConfig(self,properties):
        
        for key in properties.getKeysLower():
            try:
                code = self.color.getCode(properties.getValue(key))
            except:
                continue
            if key == "warn":
                self.warn = code
            elif key == "info":
                self.info = code
            elif key == "error":
                self.error = code
            elif key == "fatal":
                self.fatal = code
            elif key == "debug":
                self.debug = code
