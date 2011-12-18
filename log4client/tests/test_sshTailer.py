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


import unittest,logging
import os
from log4tailer.propertyparser import Property
from log4tailer import notifications
from log4tailer.sshlogtailer import SSHLogTailer
from log4tailer.configuration import DefaultConfig

class TestSSHTailer(unittest.TestCase):

    def setUp(self):
        self.configfile = 'sshconfigfile.txt'

    def _getDefaults(self):
        defaults = DefaultConfig()
        defaults.actions = [notifications.Print()]
        return defaults

    def _setUpConfigFile(self):
        fh = open(self.configfile,'w')
        fh.write('sshhostnames = hostname0, hostname1, hostname2\n')
        fh.write('hostname0 = username, /var/log/anylog555, /var/log/anylog1\n')
        fh.write('hostname1 = username, /var/log/anylog0, /var/log/anylog1\n')
        fh.write('hostname2 = username, /var/log/anylog0, /var/log/anylog1\n')
        fh.close()

    def testShouldHaveUsernameandAtLeastOneHostnameSetUp(self):
        self._setUpConfigFile()
        properties = Property(self.configfile)
        properties.parse_properties()
        logging.debug(properties.get_keys())
        defaults = self._getDefaults()
        defaults.properties = properties
        logtailer = SSHLogTailer(defaults)
        self.assertTrue(logtailer.sanityCheck())

    def testIfParametersNotProvidedShouldExit(self):
        fh = open('wrongconfigfile','w')
        fh.write('anything = anything\n')
        fh.close()
        properties = Property('wrongconfigfile')
        properties.parse_properties()
        defaults = self._getDefaults()
        defaults.properties = properties
        logtailer = SSHLogTailer(defaults)
        self.assertFalse(logtailer.sanityCheck())

    def testItShouldhaveBuildADictWithAllParamsIfAllParametersOk(self):
        self._setUpConfigFile()
        properties = Property(self.configfile)
        properties.parse_properties()
        logging.debug(properties.get_keys())
        defaults = self._getDefaults()
        defaults.properties = properties
        logtailer = SSHLogTailer(defaults)
        logtailer.sanityCheck()
        self.assertEquals(3,len(logtailer.hostnames.keys()))
        self.assertEquals('username',
                logtailer.hostnames['hostname0']['username'])

    def testshouldBuildCommandTailBasedOnHostnamesDict(self):
        self._setUpConfigFile()
        properties = Property(self.configfile)
        properties.parse_properties()
        logging.debug(properties.get_keys())
        defaults = self._getDefaults()
        defaults.properties = properties
        logtailer = SSHLogTailer(defaults)
        logtailer.sanityCheck()
        command = "tail -F /var/log/anylog555 /var/log/anylog1"
        logtailer.createCommands()
        self.assertEquals(command,logtailer.hostnames['hostname0']['command'])

    def tearDown(self):
        if os.path.exists('wrongconfigfile'):
            os.remove('wrongconfigfile')
        if os.path.exists(self.configfile):
            os.remove(self.configfile)
