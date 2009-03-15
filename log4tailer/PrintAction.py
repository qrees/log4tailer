import os

class PrintAction:

    def __init__(self):
        pass
    
    def triggerAction(self,message):
        '''msg should be colorized already
        there is a module in pypy colorize, check it out'''
        print message.getColorizedMessage();



