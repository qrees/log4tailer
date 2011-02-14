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


import getpass
from log4tailer import notifications

def setup_mail(properties):
    username = properties.get_value("mail_username")
    hostname = properties.get_value("mail_hostname")
    port = properties.get_value("mail_port") or 25
    ssl = properties.get_value("mail_ssl")
    mail_from = properties.get_value("mail_from")
    mail_to = properties.get_value("mail_to")
    password = getpass.getpass()
    mailAction = notifications.Mail(mail_from, mail_to, hostname, username,
            password, port, ssl) 
    mailAction.connectSMTP()
    return mailAction


