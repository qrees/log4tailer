import testtools
import os,sys
import fudge
SYSOUT = sys.stdout
sys.path.append('..')
from log4tailer.Log import Log
from log4tailer.Message import Message
from log4tailer.Properties import Property
from log4tailer.LogColors import LogColors
from log4tailer.Actions.PrintAction import PrintAction
from log4tailer.TermColorCodes import TermColorCodes

class Writer:
    def __init__(self):
        self.captured = []

    def __len__(self):
        return len(self.captured)

    def write(self, txt):
        self.captured.append(txt)

class TestColors(testtools.TestCase):
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
        termcolors = TermColorCodes()
        target = None
        action = PrintAction()
        message = Message(logcolors,target)
        log = Log(self.logfile)
        log.openLog()
        sys.stdout = Writer()
        #testing Colors with default pauseModes
        for count in range(len(self.someLogTraces)):
            line = log.readLine()
            line = line.rstrip()
            level = line.split('>')
            message.parse(line,log.getOptionalParameters())
            output = logcolors.getLevelColor(level[0])+line+termcolors.reset
            action.triggerAction(message,log)
            self.assertIn(output, sys.stdout.captured)
        
        line = log.readLine()
        self.assertEqual('',line)
        message.parse(line,log.getOptionalParameters())
        self.assertFalse(action.triggerAction(message,log))
    
    def testshouldColorizefirstLevelFoundignoringSecondinSameTrace(self):
        # Test for fix 5
        # Should give priority to FATAL in next trace
        level = 'FATAL'
        trace = "FATAL there could be an error in the application"
        sys.stdout = Writer()
        logcolors = LogColors()
        termcolors = TermColorCodes()
        message = Message(logcolors)
        action = PrintAction()
        anylog = Log('out.log')
        message.parse(trace,(None,None,None))
        output = logcolors.getLevelColor(level)+trace+termcolors.reset
        action.triggerAction(message,anylog)
        self.assertEqual(output, sys.stdout.captured[0])

    def testshouldNotColorizeifLevelKeyInaWord(self):
        # Testing boundary regex as for suggestion of 
        # Carlo Bertoldi
        trace = "this is a logtrace where someinfoword could be found"
        sys.stdout = Writer()
        logcolors = LogColors()
        message = Message(logcolors)
        action = PrintAction()
        anylog = Log('out.log')
        message.parse(trace,(None,None,None))
        action.triggerAction(message,anylog)
        self.assertEqual(trace, sys.stdout.captured[0])
        self.assertEqual('', message.getMessageLevel())        
    
    @fudge.with_fakes    
    def testLogColorsParseConfig(self):
        logcolors = LogColors()
        properties = fudge.Fake()
        properties = properties.provides('getKeys').returns(['one', 'two'])
        properties = properties.provides('getValue')
        properties = properties.returns('john')
        properties = properties.next_call().returns('joe')
        logcolors.parseConfig(properties)
        self.assertFalse(hasattr(logcolors,'one'))
        self.assertFalse(hasattr(logcolors,'two'))

    def testshouldColorizeMultilineLogTraces(self):
        trace = 'FATAL> something went wrong\nin here as well'
        trace0, trace1 = trace.split('\n')
        level = 'FATAL'
        termcolors = TermColorCodes()
        # now assert trace0 and trace1 are in FATAL level
        sys.stdout = Writer()
        logcolors = LogColors()
        message = Message(logcolors)
        action = PrintAction()
        anylog = Log('out.log')
        expectedLogTrace0 = logcolors.getLevelColor(level) + \
                trace0 + termcolors.reset
        expectedLogTrace1 = logcolors.getLevelColor(level) + \
                trace1 + termcolors.reset
        message.parse(trace0,(None,None,None))
        action.triggerAction(message, anylog)
        self.assertEqual(expectedLogTrace0, sys.stdout.captured[0])
        self.assertEqual('FATAL', message.getMessageLevel())        
        message.parse(trace1,(None,None,None))
        action.triggerAction(message, anylog)
        self.assertEqual(expectedLogTrace1, sys.stdout.captured[2])
        self.assertEqual('FATAL', message.getMessageLevel())        

    def tearDown(self):
        sys.stdout = SYSOUT
        os.remove(self.logfile)

#if __name__ == '__main__':
        #unittest.main()



