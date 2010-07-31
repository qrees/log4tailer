from django.db import models

class Log(models.Model):
    logpath = models.CharField(max_length=200)
    logtrace = models.CharField(max_length=1000)
    
    def __unicode__(self):
        return self.logpath
        
    #def save(self, force_insert=False, force_update=False):
        
