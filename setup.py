# Log4Tailer: A multicolored python tailer for log4J logs
# Copyright (C) 2008 Jordi Carrillo Bosch
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

import sys 

try:
    from distutils.core import setup
except:
    print "You need to install distutils python module"
    sys.exit()

PACKAGES = ("Actions Analytics").split()

setup(name="log4tailer",
      version="1.1",
      description="Not just a simple log tailer",
      author="Jordi Carrillo",
      author_email = "jordilin@gmail.com",
      url = "http://code.google.com/p/log4tailer/",
      license = "GNU GPL v3",
      packages=["log4tailer"] + map("log4tailer.".__add__,PACKAGES),
      scripts = ["log4tail"])
