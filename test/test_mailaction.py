import sys,unittest,mox,email
from exceptions import ImportError

sys.path.append('..')
from log4tailer.Actions.MailAction import MailAction

class TestMailAction(unittest.TestCase):

    def setUp(self):
        pass
    
    def testshouldBeFineImportingformatdate(self):
        mailaction = MailAction()
        self.assertTrue(mailaction.getNow())
    
    def testshoulGetNowDateFromTime(self):
        m = mox.Mox()
        mailaction = MailAction()
        m.StubOutWithMock(email.utils,'formatdate')
        email.utils.__delattr__('formatdate')
        m.ReplayAll()
        now = mailaction.getNow()
        if now:
            m.UnsetStubs()
            m.VerifyAll()
            pass
        else:
            self.fail()
    
    def tearDown(self):
        pass

if __name__=='__main__':
    unittest.main()
