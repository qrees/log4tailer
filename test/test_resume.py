import unittest
import os,sys

sys.path.append('..')
from log4tailer.Analytics import Resume
from log4tailer.Log import Log
from log4tailer.Properties import Property
from log4tailer.Message import Message
from log4tailer.LogColors import LogColors
from log4tailer.Actions.PrintAction import PrintAction
from log4tailer.Actions.MailAction import MailAction

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
        
        logline = 'this is a target line and should be reported'
        message_mocker = mox.Mox()
        message = message_mocker.CreateMock(Message)
        message.getMessageLevel().AndReturn('INFO')
        message.getPlainMessage().AndReturn((logline,'out.log'))
        message.isATarget().AndReturn(True)
        message_mocker.ReplayAll()
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
    
    def testShouldSetupMailNotificationIfAnalyticsNotificationIsSetup(self):
        fh = open('aconfig','w')
        fh.write('analyticsnotification = mail\n')
        fh.write('analyticsgaptime = 3600\n')
        fh.close()
        properties = Property('aconfig')
        properties.parseProperties()
        self.assertTrue(properties.isKey('analyticsnotification'))
        arrayLog = [Log('out.log')]
        resume = Resume.Resume(arrayLog)
        mailactionmocker = mox.Mox()
        mailaction = mailactionmocker.CreateMock(MailAction)
        if properties.getValue('analyticsnotification') == 'mail':
            resume.setMailNotification(mailaction)
            self.assertEquals('mail',resume.getNotificationType())
            gaptime = properties.getValue('analyticsgaptime')
            if gaptime:
                resume.setAnalyticsGapNotification(gaptime)
                self.assertEquals(3600,int(resume.getGapNotificationTime()))
        os.remove('aconfig')

    def tearDown(self):
        os.remove('out.log')
        os.remove('out2.log')

if __name__ == '__main__':
    unittest.main()



