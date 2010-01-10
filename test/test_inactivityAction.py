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


import unittest, testtools
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
from log4tailer.Log import Log

class Options:
    def __init__(self):
        self.inactivity = None

    @property
    def inactivity(self):
        return self.inactivity
    
    @inactivity.setter
    def inactivity(self,value):
        self.inactivity = value

class Writer():
    def __init__(self):
        self.capt = []

    def __len__(self):
        return len(self.capt)

    def write(self, txt):
        self.capt.append(txt)



class TestInactivityAction(testtools.TestCase):
    '''test that we print an alert to stdout
    once we expire the inactivity time'''

    def setUp(self):
        self.message_mocker = mox.Mox()
        self.options = Options()
        self.options.inactivity = 1
        self.log = Log('out.log',None,self.options)
        sys.stdout = Writer()

    def testSendingAlertBeyondInactivityTime(self):
        message = self.message_mocker.CreateMock(Message)
        # when there is no message, inactivity action 
        # is triggered if ellapsed time is greater than
        # inactivity time
        message.getPlainMessage().AndReturn((None,'logpath'))
        self.message_mocker.ReplayAll()
        inactivityTime = 0.0000001
        inactivityAction = InactivityAction(inactivityTime)
        time.sleep(0.0000002)
        timer = self.log.getInactivityTimer()
        self.assertTrue(timer.inactivityEllapsed() > inactivityTime)
        inactivityAction.triggerAction(message,self.log)
        self.assertIn('Inactivity', sys.stdout.capt[0])
        self.message_mocker.VerifyAll()

    
    def testNotSendingAlertBelowInactivityTime(self):

        message = self.message_mocker.CreateMock(Message)
        message.getPlainMessage().AndReturn(('error> this is an error message','logpath'))
        self.message_mocker.ReplayAll()
        inactivityTime = 0.0005
        inactivityAction = InactivityAction(inactivityTime)
        self.options.inactivity = inactivityTime
        timer = self.log.getInactivityTimer()
        time.sleep(0.000000001)
        self.assertTrue(timer.inactivityEllapsed() < inactivityTime)
        inactivityAction.triggerAction(message,self.log)
        self.assertTrue(len(sys.stdout) == 0)
        self.message_mocker.VerifyAll()

    def testInactivityTimeCanBeFloatingPointNumberSeconds(self):
        message = self.message_mocker.CreateMock(Message)
        
        # when there is no message, inactivity action 
        # is triggered if ellapsed time is greater than
        # inactivity time
        message.getPlainMessage().AndReturn((None,'logpath'))
        self.message_mocker.ReplayAll()
        inactivityAction = InactivityAction(0.0000002543)
        self.options.inactivity = 0.0000002543
        time.sleep(0.0000003)
        inactivityAction.triggerAction(message,self.log)
        self.assertIn('Inactivity', sys.stdout.capt[0])
        self.message_mocker.VerifyAll()


    def testShouldGetInactivityNotificationTypeifInConfigFile(self):
        fh = open('config.txt','w')
        fh.write('inactivitynotification = mail\n')
        fh.close()
        property = Property('config.txt')
        property.parseProperties()
        inactivityAction = InactivityAction(1,property)
        self.assertEqual('mail',inactivityAction.getNotificationType())
        os.remove('config.txt')

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
        os.remove('config.txt')

if __name__ == '__main__':
        unittest.main()


