import unittest
import os,sys

sys.path.append('..')
from log4tailer.Analytics import Resume
from log4tailer.Log import Log
from log4tailer.Message import Message
from log4tailer.LogColors import LogColors
from log4tailer.Actions.PrintAction import PrintAction
import mox

class TestResume(unittest.TestCase):

    def writer(self,fh,logTraces):
        for line in logTraces:
            fh.write(line+'\n')

    def setUp(self):
        fh = open('out.log','w')
        someLogTracesForOutLog = ['fatal> something went wrong',
                              'error> not so wrong',
                              'warn> be careful',
                              'debug> looking behind the scenes',
                              'info> the app is running',
                              'fatal> the app is in really bad state']
        
        someLogTracesForOut2Log = ['fatal> something went wrong',
                              'error> not so wrong',
                              'warn> be careful',
                              'debug> looking behind the scenes',
                              'info> the app is running',
                              'fatal> the app is in really bad state']

        fh2 = open('out2.log','w')
        self.writer(fh,someLogTracesForOutLog)
        self.writer(fh2,someLogTracesForOut2Log)
        
        fh.close()
        fh2.close()
    

    def readAndUpdateLines(self,log,message,resume):
        fh = log.openLog()
        lines = [ line.rstrip() for line in fh.readlines() ]
        for line in lines:
            message.parse(line,log.getOptionalParameters())
            resume.update(message,log)

    def testReportResumeForTwoDifferentLogs(self):
        log = Log('out.log')
        log2 = Log('out2.log')
        arrayLogs = [log,log2]
        fh = log.openLog()
        logcolors = LogColors()
        message = Message(logcolors)
        resume = Resume.Resume(arrayLogs)
        for anylog in arrayLogs:
            self.readAndUpdateLines(anylog,message,resume)
         
        print "you should see the resume output"
        resume.report()

    
    def testShouldReportaTarget(self):
        message_mocker = mox.Mox()
        message = message_mocker.CreateMock(Message)
        message.getMessageLevel().AndReturn('INFO')
        message.isATarget().AndReturn(True)
        message_mocker.ReplayAll()
        logline = 'this is a target line and should be reported'
        mylog = Log('out.log')
        arraylogs = [mylog]
        resume = Resume.Resume(arraylogs)
        resume.update(message,mylog)
        print "you should see a target found in report"
        resume.report()
    
    def testTargetsAreNonTimeStampedinResume(self):
        arrayLog = [Log('out.log')]
        resume = Resume.Resume(arrayLog)
        self.assertTrue('TARGET' in resume.nonTimeStamped)
        self.assertTrue('TARGET' in resume.orderReport)

    def tearDown(self):
        os.remove('out.log')

if __name__ == '__main__':
    unittest.main()



