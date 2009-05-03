class PauseMode:
    '''In PrintAction if an specific
    level is found, it will pause so we will
    not miss a level'''

    def __init__(self):
        self.defaultLevelPauses = {'DEBUG':0,'INFO':0, 'WARN':2, 'ERROR':3, 'FATAL':5, 'TARGET':5}

    def getPause(self,level):
        return self.defaultLevelPauses[level]

    def parseConfig(self,properties):
        pauseKeys = ['pauseDEBUG','pauseINFO','pauseWARN','pauseERROR','pauseFATAL','pauseTARGET']
        for pauseKey in pauseKeys:
            try:
                level = pauseKey.split('pause')[1]
                pauseLevel = float(properties.getValue(pauseKey))
                self.defaultLevelPauses[level] = pauseLevel
            except:
                pass
