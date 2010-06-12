import unittest
import os,sys
import time
sys.path.append('..')
from log4tailer import reporting
from log4tailer.Log import Log
from log4tailer.Properties import Property
from log4tailer.Message import Message
from log4tailer.LogColors import LogColors
from log4tailer import notifications

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
            message.parse(line, log)
            resume.update(message, log)

    def testReportResumeForTwoDifferentLogs(self):
        log = Log('out.log')
        log2 = Log('out2.log')
        arrayLogs = [log]
        fh = log.openLog()
        logcolors = LogColors()
        message = Message(logcolors)
        resume = reporting.Resume(arrayLogs)
        for anylog in arrayLogs:
            self.readAndUpdateLines(anylog,message,resume)
        
        outlogReport = resume.logsReport[log.getLogPath()]
        expectedOutLogErrorReport = 'error> not so wrong'
        gotLogTrace = outlogReport['ERROR'][0].split('=>> ')[1]
        self.assertEquals(expectedOutLogErrorReport,
                gotLogTrace)
               
    
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
        resume = reporting.Resume(arraylogs)
        resume.update(message,mylog)
        outLogReport = resume.logsReport[mylog.getLogPath()]
        numofTargets = 1
        gotnumTargets = outLogReport['TARGET']
        self.assertEquals(numofTargets, gotnumTargets)
        message_mocker.VerifyAll()
    
    def testTargetsAreNonTimeStampedinResume(self):
        arrayLog = [Log('out.log')]
        resume = reporting.Resume(arrayLog)
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
        resume = reporting.Resume(arrayLog)
        mailactionmocker = mox.Mox()
        mailaction = mailactionmocker.CreateMock(notifications.Mail)
        if properties.getValue('analyticsnotification') == 'mail':
            resume.setMailNotification(mailaction)
            self.assertEquals('mail',resume.getNotificationType())
            gaptime = properties.getValue('analyticsgaptime')
            if gaptime:
                resume.setAnalyticsGapNotification(gaptime)
                self.assertEquals(3600,int(resume.getGapNotificationTime()))
        os.remove('aconfig')

    def testReportToAFile(self):
        reportfileFullPath = "reportfile.txt"
        fh = open('aconfig','w')
        fh.write('analyticsnotification = '+ reportfileFullPath +'\n')
        fh.write('analyticsgaptime = 0.1\n')
        fh.close()
        properties = Property('aconfig')
        properties.parseProperties()
        self.assertTrue(properties.isKey('analyticsnotification'))
        log = Log('out.log')
        arrayLog = [log]
        resume = reporting.Resume(arrayLog)
        resume.setAnalyticsGapNotification(0.1)
        resume.notification_type(reportfileFullPath)
        fh = open('out.log')
        lines = fh.readlines()
        fh.close()
        logcolors = LogColors()
        msg = Message(logcolors)
        time.sleep(0.1)
        for line in lines:
            msg.parse(line, log)
            resume.update(msg, log)
        fh = open(reportfileFullPath)
        reportlength = len(fh.readlines())
        fh.close()
        os.remove(reportfileFullPath)
        self.assertEquals(21, reportlength)

    def tearDown(self):
        os.remove('out.log')
        os.remove('out2.log')

if __name__ == '__main__':
    unittest.main()



