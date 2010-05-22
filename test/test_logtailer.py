import unittest
import os,sys
SYSOUT = sys.stdout
sys.path.append('..')
from log4tailer.Analytics import Resume
from log4tailer.Log import Log
from log4tailer.Message import Message
from log4tailer.LogTailer import LogTailer
from log4tailer.LogColors import LogColors
from log4tailer import notifications
from log4tailer.Properties import Property
import mox

class Writer:
    def __init__(self):
        self.captured = []

    def __len__(self):
        return len(self.captured)

    def write(self, txt):
        self.captured.append(txt)

class TestResume(unittest.TestCase):
    
    def testshouldReturnTrueifMailAlreadyinMailAction(self):
        logcolors = LogColors()
        mailActionMocker = mox.Mox()
        mailAction = mailActionMocker.CreateMock(notifications.Mail)
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
        printaction = notifications.Print()
        actions = [printaction]
        throttleTime = 0
        silence = False
        target = None
        pause = 0
        logtailer = LogTailer(logcolors, target, pause, throttleTime, silence, actions, properties)
        self.assertEqual(False,logtailer.mailIsSetup())

    
    def testshouldReturnFalseifBothMailActionOrInactivityActionNotificationNotEnabled(self):
        logcolors = LogColors()
        printaction = notifications.Print()
        actions = [printaction]
        throttleTime = 0
        silence = False
        target = None
        pause = 0
        properties = None
        logtailer = LogTailer(logcolors, target, pause, throttleTime, silence, actions, properties)
        self.assertEqual(False,logtailer.mailIsSetup())
    
    def testPipeOutShouldSendMessageParseThreeParams(self):
        sys.stdin = ['error > one error', 'warning > one warning']
        sys.stdout = Writer()
        logcolors = LogColors()
        printaction = notifications.Print()
        actions = [printaction]
        throttleTime = 0
        silence = False
        target = None
        pause = 0
        properties = None
        logtailer = LogTailer(logcolors, target, pause, throttleTime, silence, actions, properties)
        logtailer.pipeOut()
        self.assertTrue('error > one error' in sys.stdout.captured[0])

    def tearDown(self):
        sys.stdout = SYSOUT

