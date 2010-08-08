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
        


