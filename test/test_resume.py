import unittest
import os,sys

sys.path.append('..')
from log4tailer.Analytics import Resume
from log4tailer.Log import Log
from log4tailer.Message import Message
from log4tailer.LogColors import LogColors
from log4tailer.Actions.PrintAction import PrintAction

class TestColors(unittest.TestCase):
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

    def testResume(self):
        fh = open(self.logfile)
        lines = [ line.rstrip() for line in fh.readlines() ]
        resume = Resume.Resume()
        logcolors = LogColors()
        message = Message(logcolors)
        for line in lines:
            message.parse(line)
            resume.update(message.getMessageLevel())
        
        info = {'FATAL':2,
                'ERROR':1,
                'INFO':1,
                'WARN':1,
                'DEBUG':1}
        
        for key,val in info.iteritems():
            res = resume.getInfo(key)
            self.assertEqual(info[key],res)
        
        print "you should see the resume output"
        resume.spit()
        

    def tearDown(self):
        os.remove(self.logfile)

if __name__ == '__main__':
        unittest.main()



