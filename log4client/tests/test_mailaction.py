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
from log4tailer import notifications
from log4tailer import utils
from .utils import PropertiesStub


version_info = sys.version_info
version2_4 = (2, 4)
skip_from_time = False
if version_info[:2] == version2_4:
    skip_from_time = True


class TestMailAction(unittest.TestCase):

    def test_setupMail(self):
        def getpass():
            return "111"

        mailaction = utils.setup_mail(PropertiesStub(), getpass)
        self.assertTrue(isinstance(mailaction, notifications.Mail))


class SMTPStub(object):
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def login(self, user, passwd):
        pass


class SMTPStubRaise(object):
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def login(self, user, passwd):
        raise Exception("Could not login")


class SMTPFactoryStub(notifications.SMTPFactory):

    def connection_type(self):
        return SMTPStub


class SMTPFactoryStubRaise(notifications.SMTPFactory):

    def connection_type(self):
        return SMTPStubRaise


class MailTestCase(unittest.TestCase):

    def test_instantiates(self):
        mail = notifications.Mail()
        self.assertTrue(isinstance(mail, notifications.Mail))

    def test_is_ssl(self):
        mail = notifications.Mail(ssl=True)
        self.assertTrue(isinstance(mail.smtpfactory,
            notifications.SMTPFactory))

    def test_connects_login(self):
        hostname = "localhost"
        port = 3456
        user = "test"
        passwd = "test"
        mail = notifications.Mail(hostname=hostname,
                port=port, user=user, passwd=passwd,
                smtpfactory=SMTPFactoryStub)
        conn = mail.connectSMTP()
        self.assertTrue(isinstance(mail.conn, SMTPStub))

    def test_connect_raises(self):
        hostname = "localhost"
        port = 3456
        user = "test"
        passwd = "test"
        mail = notifications.Mail(hostname=hostname,
                port=port, user=user, passwd=passwd,
                smtpfactory=SMTPFactoryStubRaise)
        try:
            conn = mail.connectSMTP()
            self.fail()
        except SystemExit:
            pass


class TimeStub(object):
    def __init__(self):
        pass

    def time(self):
        pass

    def gmtime(self, current_time):
        return (2012, 02, 12, 00, 01, 01, 6, 0, 0)


class DateFormatterTestCase(unittest.TestCase):

    def test_date_time(self):
        date_formatter = notifications.DateFormatter(time=TimeStub())
        expected_format = 'Sun, 12 Feb 2012 00:01:01 GMT'
        self.assertEqual(expected_format, date_formatter.date_time())

    def test_get_now(self):
        date_formatter = notifications.DateFormatter(time=TimeStub())
