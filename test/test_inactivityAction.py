# Log4Tailer: A multicolored python tailer for log4J logs
# Copyright (C) 2008 Jordi Carrillo Bosch

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
import os,sys,time
try:
    import mox
except:
    print "you need to install the mox mocking library"
    sys.exit()

sys.path.append('..')
from log4tailer.Actions.InactivityAction import InactivityAction
from log4tailer.Actions.MailAction import MailAction
from log4tailer.Message import Message
from log4tailer.Properties import Property

class TestInactivityAction(unittest.TestCase):
    '''test that we print an alert to stdout
    once we expire the inactivity time'''

    def setUp(self):
        self.message_mocker = mox.Mox()

    def testSendingAlertBeyondInactivityTime(self):
        message = self.message_mocker.CreateMock(Message)
        
        # when there is no message, inactivity action 
        # is triggered if ellapsed time is greater than
        # inactivity time
        message.getPlainMessage().AndReturn(None)
        self.message_mocker.ReplayAll()
        inactivityAction = InactivityAction(1)
        time.sleep(2)
        print "we should see an emphasized alert in stdout"
        inactivityAction.triggerAction(message)
        self.message_mocker.VerifyAll()

    def testNotSendingAlertWeHaveAMessage(self):
        message = self.message_mocker.CreateMock(Message)
        message.getPlainMessage().AndReturn('FATAL> this is a message')
        self.message_mocker.ReplayAll()
        inactivityAction = InactivityAction(1)
        time.sleep(2)
        print "we should see nothing"
        inactivityAction.triggerAction(message)
        self.message_mocker.VerifyAll()

    def testNotSendingAlertBelowInactivityTime(self):

        message = self.message_mocker.CreateMock(Message)
        message.getPlainMessage().AndReturn('error> this is an error message')
        self.message_mocker.ReplayAll()
        inactivityAction = InactivityAction(5)
        time.sleep(1)
        print "we should see nothing"
        inactivityAction.triggerAction(message)
        self.message_mocker.VerifyAll()

    def testInactivityTimeCanBeFloatingPointNumberSeconds(self):
        message = self.message_mocker.CreateMock(Message)
        
        # when there is no message, inactivity action 
        # is triggered if ellapsed time is greater than
        # inactivity time
        message.getPlainMessage().AndReturn(None)
        self.message_mocker.ReplayAll()
        print "setting inactivity monitoring time to 2.543"
        inactivityAction = InactivityAction(2.543)
        print "sleeping for 3 secs"
        time.sleep(3)
        print "we should see an emphasized alert in stdout"
        inactivityAction.triggerAction(message)
        self.message_mocker.VerifyAll()

    def testShouldGetInactivityNotificationTypeifInConfigFile(self):
        fh = open('config.txt','w')
        fh.write('inactivitynotification = mail\n')
        fh.close()
        property = Property('config.txt')
        property.parseProperties()
        inactivityAction = InactivityAction(1,property)
        self.assertEqual('mail',inactivityAction.getNotificationType())
    
    def testShouldBePrintNotificationTypeifNoConfigFile(self):
        inactivityAction = InactivityAction(1)
        self.assertEqual('print',inactivityAction.getNotificationType())
    
    def testIfMailNotificationTypeAlreadyAvailablebyMailActionItShouldSetItUp(self):
        mailActionMocker = mox.Mox()
        mailAction = mailActionMocker.CreateMock(MailAction)
        fh = open('config.txt','w')
        fh.write('inactivitynotification = mail\n')
        fh.close()
        property = Property('config.txt')
        property.parseProperties()
        inactivityAction = InactivityAction(1,property)
        if inactivityAction.getNotificationType() == 'mail':
            # what is called inversion of control pattern actually
            inactivityAction.setMailNotification(mailAction)
        else:
            self.fail('should be inactivityAction with mail Notification') 
        
if __name__ == '__main__':
        unittest.main()


