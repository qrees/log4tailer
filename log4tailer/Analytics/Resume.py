class Resume():

    def __init__(self):
        self.levels = {'DEBUG':0,
                       'INFO':0,
                       'WARN':0,
                       'ERROR':0,
                       'FATAL':0}

    def update(self,messageLevel):
        if self.levels.has_key(messageLevel):
            self.levels[messageLevel] += 1

    def getInfo(self,messageLevel):
        return self.levels[messageLevel]

    def spit(self):
        print "Analytics: "
        for key,val in self.levels.iteritems():
            print "level "+key+": "+str(val)

                       
