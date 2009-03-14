from ColorParser import ColorParser

class Message:
    '''the message to be actioned
    and showed being by email, stdout,...'''

    def __init__(self,logcolor,patarget = None):
        
        self.patarget = patarget
        self.color = logcolor
        self.plainMessage = None
        self.colorizedMessage = None
        self.colorparser = ColorParser()
        self.messageLevel = None
    

    def getColorizedMessage(self):
        if self.patarget:
            res = self.patarget.search(self.plainMessage)
            if res:
                return self.color.backgroundemph+self.plainMessage+self.color.reset
        
        # tail the other lines (levels)
        if self.messageLevel == "WARN":
            return self.color.warn+self.plainMessage+self.color.reset
        elif self.messageLevel == "FATAL":
            return self.color.fatal+self.plainMessage+self.color.reset
        elif self.messageLevel == "INFO":
            return self.color.info+self.plainMessage+self.color.reset
        elif self.messageLevel == "ERROR":
            return self.color.error+self.plainMessage+self.color.reset
        elif self.messageLevel == "DEBUG":
            return self.color.debug+self.plainMessage+self.color.reset
        else:
            return line

    def getMessageLevel(self):
        return self.messageLevel


    def getPlainMessage(self):
        return self.plainMessage
    
    def parse(self,line):
        '''Need to parse the line
        and check in what level we are in'''
        
        self.plainMessage = line
        self.messageLevel = self.colorparser.parse(line)
        
                

   
        
        

