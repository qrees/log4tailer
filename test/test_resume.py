import unittest
import os,sys

sys.path.append('..')
from log4tailer.Analytics import Resume
from log4tailer.Log import Log
from log4tailer.Message import Message
from log4tailer.LogColors import LogColors
from log4tailer.Actions.PrintAction import PrintAction

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
            message.parse(line,log.getOwnOutputColor())
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
      

    def tearDown(self):
        os.remove('out.log')

if __name__ == '__main__':
    unittest.main()



