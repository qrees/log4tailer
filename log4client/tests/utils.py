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


class MemoryWriter(object):
    def __init__(self):
        self.captured = []

    def __len__(self):
        return len(self.captured)

    def write(self, txt):
        self.captured.append(txt)

    def flush(self):
        self.captured = []

    def fileno(self):
        return True


class MemoryReader(object):
    def __init__(self):
        pass

    def fileno(self):
        return True

    def __getattr__(self, method):
        pass


class SubProcessStub(object):
    msg = "called..."

    def __init__(self):
        pass

    @staticmethod
    def call(*args, **kwargs):
        print SubProcessStub.msg


class SubProcessStubRaise(object):
    msg = "Boo, it failed"

    def __init__(self):
        pass

    @staticmethod
    def call(*args, **kwargs):
        raise Exception(SubProcessStubRaise.msg)
