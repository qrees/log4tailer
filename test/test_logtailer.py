import unittest
import os,sys

sys.path.append('..')
from log4tailer.Analytics import Resume
from log4tailer.Log import Log
from log4tailer.Message import Message
from log4tailer.LogTailer import LogTailer
from log4tailer.LogColors import LogColors
from log4tailer.Actions.PrintAction import PrintAction
from log4tailer.Actions.MailAction import MailAction
from log4tailer.Properties import Property
import mox

class TestResume(unittest.TestCase):
    
    def testshouldReturnTrueifMailAlreadyinMailAction(self):
        logcolors = LogColors()
        mailActionMocker = mox.Mox()
        mailAction = mailActionMocker.CreateMock(MailAction)
        actions = [mailAction]
        throttleTime = 0
        silence = False
        target = None
        pause = 0
        properties = None
        logtailer = LogTailer(logcolors, target, pause, throttleTime, silence, actions, properties)
        self.assertEqual(True,logtailer.mailIsSetup())


    def __setupAConfig(self):
        fh = open('aconfig','w')
        fh.write('inactivitynotification = mail\n')
        fh.close()

    def testshouldReturnFalseifPropertiesHasInactivityActionNotificationSetToMailbutNoInactivityActionPassed(self):
        self.__setupAConfig()
        properties = Property('aconfig')
        properties.parseProperties()
        logcolors = LogColors()
        printaction = PrintAction()
        actions = [printaction]
        throttleTime = 0
        silence = False
        target = None
        pause = 0
        logtailer = LogTailer(logcolors, target, pause, throttleTime, silence, actions, properties)
        self.assertEqual(False,logtailer.mailIsSetup())

    
    def testshouldReturnFalseifBothMailActionOrInactivityActionNotificationNotEnabled(self):
        logcolors = LogColors()
        printaction = PrintAction()
        actions = [printaction]
        throttleTime = 0
        silence = False
        target = None
        pause = 0
        properties = None
        logtailer = LogTailer(logcolors, target, pause, throttleTime, silence, actions, properties)
        self.assertEqual(False,logtailer.mailIsSetup())
    
    #def testShouldReturnTrueifAnalyticsNotification


if __name__ == '__main__':
    unittest.main()



