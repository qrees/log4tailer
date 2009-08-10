import unittest
import os,sys

sys.path.append('..')
from log4tailer.Log import Log
from log4tailer.Message import Message
from log4tailer.LogColors import LogColors
from log4tailer.Actions.PrintAction import PrintAction

class TestColors(unittest.TestCase):
    def setUp(self):
        self.logfile = 'out.log'
        fh = open(self.logfile,'w')
        # levels in upper case
        # should be very weird an app
        # logging levels in lowercase

        self.someLogTraces = ['FATAL> something went wrong',
                              'ERROR> not so wrong',
                              'WARN> be careful',
                              'DEBUG> looking behind the scenes',
                              'INFO> the app is running']
        for line in self.someLogTraces:
            fh.write(line+'\n')
        fh.close()

    def testMessage(self):
        logcolors = LogColors() #using default colors
        target = None
        action = PrintAction()
        message = Message(logcolors,target)
        log = Log(self.logfile)
        log.openLog()
        print "testing Colors with default pauseModes"
        for count in range(len(self.someLogTraces)):
            line = log.readLine()
            line = line.rstrip()
            message.parse(line,log.getOptionalParameters())
            action.triggerAction(message)
        
        line = log.readLine()
        self.assertEqual('',line)
        message.parse(line,log.getOptionalParameters())
        print "nothing in next line"
        action.triggerAction(message)
        print ""
    
    def testshouldColorizefirstLevelFoundignoringSecondinSameTrace(self):
        # Test for fix 5
        # Should give priority to FATAL in next trace
        trace = "FATAL there could be an error in the application"
        logcolors = LogColors()
        message = Message(logcolors)
        action = PrintAction()
        
        message.parse(trace,(None,None))
        print "Test: You should see a red log trace now: "
        action.triggerAction(message)

    def tearDown(self):
        os.remove(self.logfile)

if __name__ == '__main__':
        unittest.main()



