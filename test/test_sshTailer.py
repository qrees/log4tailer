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


import unittest,logging
import os
import sys
sys.path.append('..')
from log4tailer.LogColors import LogColors
from log4tailer.Properties import Property
from log4tailer import notifications
from log4tailer.SSHLogTailer import SSHLogTailer

class TestSSHTailer(unittest.TestCase):

    def setUp(self):
        self.configfile = 'sshconfigfile.txt'

    def __setUpConfigFile(self):
        fh = open(self.configfile,'w')
        fh.write('sshhostnames = hostname0, hostname1, hostname2\n')
        fh.write('hostname0 = username, /var/log/anylog555, /var/log/anylog1\n')
        fh.write('hostname1 = username, /var/log/anylog0, /var/log/anylog1\n')
        fh.write('hostname2 = username, /var/log/anylog0, /var/log/anylog1\n')
        fh.close()

    def testShouldHaveUsernameandAtLeastOneHostnameSetUp(self):
        self.__setUpConfigFile()
        properties = Property(self.configfile)        
        properties.parseProperties()
        logging.debug(properties.getKeys())
        logcolors = LogColors()
        printaction = notifications.Print()
        actions = [printaction]
        throttleTime = 0
        silence = False
        target = None
        pause = 0
        logtailer = SSHLogTailer(logcolors, target, pause, throttleTime, silence, actions, properties)
        self.assertTrue(logtailer.sanityCheck())
    
    def testIfParametersNotProvidedShouldExit(self):
        fh = open('wrongconfigfile','w')
        fh.write('anything = anything\n')
        fh.close()
        properties = Property('wrongconfigfile')
        properties.parseProperties()
        logtailer = SSHLogTailer(LogColors(),None,0,0,False,notifications.Print(),properties)
        self.assertFalse(logtailer.sanityCheck())
        os.remove('wrongconfigfile')
    
    def testItShouldhaveBuildADictWithAllParamsIfAllParametersOk(self):
        self.__setUpConfigFile()
        properties = Property(self.configfile)        
        properties.parseProperties()
        logging.debug(properties.getKeys())
        logcolors = LogColors()
        printaction = notifications.Print()
        actions = [printaction]
        throttleTime = 0
        silence = False
        target = None
        pause = 0
        logtailer = SSHLogTailer(logcolors, target, pause, throttleTime, silence, actions, properties)
        logtailer.sanityCheck()
        self.assertEquals(3,len(logtailer.hostnames.keys()))
        self.assertEquals('username',logtailer.hostnames['hostname0']['username'])
    
    def testshouldBuildCommandTailBasedOnHostnamesDict(self):
        self.__setUpConfigFile()
        properties = Property(self.configfile)        
        properties.parseProperties()
        logging.debug(properties.getKeys())
        logcolors = LogColors()
        printaction = notifications.Print()
        actions = [printaction]
        throttleTime = 0
        silence = False
        target = None
        pause = 0
        logtailer = SSHLogTailer(logcolors, target, pause, throttleTime, silence, actions, properties)
        logtailer.sanityCheck()
        command = "tail -F /var/log/anylog555 /var/log/anylog1"
        logtailer.createCommands()
        self.assertEquals(command,logtailer.hostnames['hostname0']['command'])

    def tearDown(self):
        if os.path.exists(self.configfile):
            os.remove(self.configfile)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    unittest.main()
        

