import os,time

class PrintAction:

    def __init__(self):
        pass
    
    def triggerAction(self,message):
        '''msg should be colorized already
        there is a module in pypy colorize, check it out'''
        (pause, colormsg) = message.getColorizedMessage()
        if colormsg:
            print colormsg
            time.sleep(pause)

    def printInit(self,message):
        (pause,colormsg) = message.getColorizedMessage()
        pause = 0
        if colormsg:
            print colormsg




