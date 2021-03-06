# Log4Tailer: A multicolored python tailer for log4J logs
# Copyright (C) 2010 Jordi Carrillo Bosch

# This file is part of Log4Tailer Project.
#
# Log4Tailer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Log4Tailer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Log4Tailer.  If not, see <http://www.gnu.org/licenses/>.


import unittest
import os
import sys
import time
import mocker
import mox
from log4tailer import notifications
from log4tailer.message import Message
from log4tailer.propertyparser import Property
from log4tailer.logfile import Log
from .utils import MemoryWriter

SYSOUT = sys.stdout


class Options:
    def __init__(self):
        self.inactivity = None


def overgap():
    return 0.06


def belowgap():
    return 0.00001


class TestInactivityAction(unittest.TestCase):
    '''test that we print an alert to stdout
    once we expire the inactivity time'''

    def setUp(self):
        self.message_mocker = mox.Mox()
        self.options = Options()
        self.options.inactivity = 1
        self.log = Log('out.log',None,self.options)
        self.mocker = mocker.Mocker()

    def testSendingAlertBeyondInactivityTime(self):
        sys.stdout = MemoryWriter()
        message = self.message_mocker.CreateMock(Message)
        # when there is no message, inactivity action 
        # is triggered if ellapsed time is greater than
        # inactivity time
        message.getPlainMessage().AndReturn((None,'logpath'))
        self.message_mocker.ReplayAll()
        inactivityTime = 0.01
        notifier = notifications.Inactivity(inactivityTime)
        self.log.inactivityTimer.inactivityEllapsed = overgap
        notifier.notify(message, self.log)
        self.assertTrue('Inactivity' in sys.stdout.captured[0])
        self.message_mocker.VerifyAll()
    
    def testNotSendingAlertBelowInactivityTime(self):
        sys.stdout = MemoryWriter()
        self.message_mocker.ReplayAll()
        inactivityTime = 0.01
        class Message(object):
            def __init__(self):
                pass
            def getPlainMessage(self):
                return (None, "alog")
                
        notifier = notifications.Inactivity(inactivityTime)
        self.options.inactivity = inactivityTime
        self.log.inactivityTimer.inactivityEllapsed = belowgap
        notifier.notify(Message(), self.log)
        self.assertTrue(len(sys.stdout.captured) == 0)
        self.message_mocker.VerifyAll()

    def testInactivityTimeCanBeFloatingPointNumberSeconds(self):
        sys.stdout = MemoryWriter()
        message = self.message_mocker.CreateMock(Message)
        
        # when there is no message, inactivity action 
        # is triggered if ellapsed time is greater than
        # inactivity time
        message.getPlainMessage().AndReturn((None,'logpath'))
        self.message_mocker.ReplayAll()
        notifier = notifications.Inactivity(0.0000002543)
        self.options.inactivity = 0.0000002543
        self.log.inactivityTimer.inactivityEllapsed = overgap
        notifier.notify(message, self.log)
        self.assertTrue('Inactivity' in sys.stdout.captured[0])
        self.assertTrue(notifier.alerted)
        self.message_mocker.VerifyAll()

    def testShouldGetInactivityNotificationTypeifInConfigFile(self):
        fh = open('config.txt','w')
        fh.write('inactivitynotification = mail\n')
        fh.close()
        property = Property('config.txt')
        property.parse_properties()
        notifier = notifications.Inactivity(1,property)
        self.assertEqual('mail',notifier.getNotificationType())
        os.remove('config.txt')

    def testShouldBePrintNotificationTypeifNoConfigFile(self):
        notifier = notifications.Inactivity(1)
        self.assertEqual('print',notifier.getNotificationType())
    
    def testIfMailNotificationTypeAlreadyAvailablebyMailShouldSetItUp(self):
        mailMocker = mox.Mox()
        mail = mailMocker.CreateMock(notifications.Mail)
        fh = open('config.txt','w')
        fh.write('inactivitynotification = mail\n')
        fh.close()
        property = Property('config.txt')
        property.parse_properties()
        notifier = notifications.Inactivity(1,property)
        if notifier.getNotificationType() == 'mail':
            notifier.setMailNotification(mail)
        else:
            self.fail('should be notifier with mail Notification') 
        os.remove('config.txt')

    def testalerted_not_alerted(self):
        options = Options()
        options.inactivity =  0.05
        log = Log('out.log', None, options)
        message_mock = self.mocker.replace('log4tailer.message.Message')
        message_mock.getPlainMessage()
        self.mocker.count(1, None)
        self.mocker.result(('', 'logpath'))
        inactivityTime = 0.05
        notifier = notifications.Inactivity(inactivityTime)
        self.mocker.replay()
        log.inactivityTimer.inactivityEllapsed = overgap
        notifier.notify(message_mock, log)
        self.assertTrue(notifier.alerted)
        log.inactivityTimer.inactivityEllapsed = belowgap
        notifier.notify(message_mock, log)
        self.assertFalse(notifier.alerted)
        notifier.notify(message_mock, log)
        log.inactivityTimer.inactivityEllapsed = overgap
        notifier.notify(message_mock, log)
        self.assertTrue(notifier.alerted)

    def tearDown(self):
        self.mocker.restore()
        self.mocker.verify()
        sys.stdout = SYSOUT

if __name__ == '__main__':
    unittest.main()


