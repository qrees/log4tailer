from django.db import models

class Log(models.Model):
    logpath = models.CharField(max_length=200, blank = False)
    server = models.CharField(max_length=200, blank = False)
    
    def __unicode__(self):
        return self.logpath

class LogTrace(models.Model):
    logtrace = models.ForeignKey(Log)
    
    def __unicode__(self):
        return self.logtrace
        
