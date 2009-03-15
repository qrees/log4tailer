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


import sys
class TermColorCodes:
    '''Defines the ANSI Terminal
    color codes'''
    def __init__(self):
        self.esc = "\033["
        self.black = self.esc+"30m"
        self.red = self.esc+"31m"
        self.green = self.esc+"32m"
        self.yellow = self.esc+"33m"
        self.blue = self.esc+"34m"
        self.magenta = self.esc+"35m"
        self.cyan = self.esc+"36m"
        self.white = self.esc+"37m"
        self.reset = self.esc+"0m"
        self.backgroundemph = self.esc+"41m"

    def getCode(self,value):
        '''Returns the color code
        provided the ascii color word'''
        if value == 'black':
            return self.black
        elif value == 'red':
            return self.red
        elif value == 'green':
            return self.green
        elif value == 'yellow':
            return self.yellow
        elif value == 'blue':
            return self.blue
        elif value == 'magenta':
            return self.magenta
        elif value == 'cyan':
            return self.cyan
        elif value == 'white':
            return self.white
        else:
            print "wrong config"
            sys.exit()
