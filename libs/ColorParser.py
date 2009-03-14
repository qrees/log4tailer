import re

class ColorParser:
    def __init__(self):
        
        self.debug = re.compile(r'debug',re.I)
        self.info = re.compile(r'info',re.I)
        self.warn = re.compile(r'warn',re.I)
        self.error = re.compile(r'error',re.I)
        self.fatal = re.compile(r'fatal',re.I)
        
    def parse(self,line):
        if (self.debug.search(line)):
            return 'DEBUG'
        elif (self.info.search(line)):
            return 'INFO'
        elif (self.warn.search(line)):
            return 'WARN'
        elif (self.error.search(line)):
            return 'ERROR'
        elif (self.fatal.search(line)):
            return 'FATAL'
        else:
            return ''