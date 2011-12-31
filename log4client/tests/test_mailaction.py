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

import sys
import unittest
import email
import mocker
import decorators as dec
from log4tailer import notifications
from log4tailer import utils
from .utils import PropertiesStub


version_info = sys.version_info
version2_4 = (2, 4)
skip_from_time = False
if version_info[:2] == version2_4:
    skip_from_time = True


class TestMailAction(unittest.TestCase):

    def setUp(self):
        self.mocker = mocker.Mocker()

    def testshouldBeFineImportingformatdate(self):
        mailaction = notifications.Mail()
        self.assertTrue(mailaction.getNow())

    @dec.skipif(skip_from_time, "invalid for 2.4")
    def testshoulGetNowDateFromTime(self):
        mailaction = notifications.Mail()
        del(email.utils.formatdate)
        now = mailaction.getNow()
        self.assertTrue(now)

    def test_setupMail(self):
        def getpass():
            return "111"

        mailaction = utils.setup_mail(PropertiesStub(), getpass)
        self.assertTrue(isinstance(mailaction, notifications.Mail))

    def tearDown(self):
        self.mocker.restore()
        self.mocker.verify()
