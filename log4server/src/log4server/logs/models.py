# Log4Tailer: A multicolored python tailer for log4J logs
# Copyright (C) 2010 Jordi Carrillo Bosch

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

from django.db import models

class Log(models.Model):
    logpath = models.CharField(max_length = 200, blank = False)
    logserver = models.CharField(max_length = 200, blank = False)
    
    def __unicode__(self):
        return self.logpath
    
    @staticmethod
    def json_mapper():
        callables = {}
        return callables

class LogTrace(models.Model):
    log = models.ForeignKey(Log, blank = False)
    logtrace = models.CharField(max_length = 1000, blank = False)
    level = models.CharField(max_length = 15, blank = False)
    insertion_date = models.DateTimeField(auto_now_add=True, auto_now=True,
            blank=False)
    
    def __unicode__(self):
        return self.logtrace

    @staticmethod
    def json_mapper():
        callables  = {'log' : Log}
        return callables
        


