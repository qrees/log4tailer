import unittest
import os,sys

sys.path.append('..')
from log4tailer.Analytics import Resume
from log4tailer.Log import Log
from log4tailer.Message import Message
from log4tailer.LogColors import LogColors
from log4tailer.Actions.PrintAction import PrintAction

class TestResume(unittest.TestCase):
    def setUp(self):
        self.logfile = 'out.log'
        fh = open(self.logfile,'w')
        self.someLogTraces = ['fatal> something went wrong',
                              'error> not so wrong',
                              'warn> be careful',
                              'debug> looking behind the scenes',
                              'info> the app is running',
                              'fatal> the app is in really bad state']
        for line in self.someLogTraces:
            fh.write(line+'\n')
        fh.close()


    def testReportResume(self):
        fh = open(self.logfile)
        lines = [ line.rstrip() for line in fh.readlines() ]
        logcolors = LogColors()
        message = Message(logcolors)
        resume = Resume.Resume()
        for line in lines:
            message.parse(line)
            resume.update(message)
        
        print "you should see the resume output"
        resume.report()
        

    def tearDown(self):
        os.remove(self.logfile)

if __name__ == '__main__':
    unittest.main()



