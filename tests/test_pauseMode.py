import unittest
import os,sys

sys.path.append('..')

from log4tailer.Actions.PauseMode import PauseMode
from log4tailer.Properties import Property
from log4tailer.log4Exceptions import KeyAlreadyExistsException,KeyNotFoundException

class TestPauseMode(unittest.TestCase):
    
    def setUp(self):
        self.configfile = 'config.txt'
        self.configfh = open(self.configfile,'w')
        
        self.overridenLevelPauses = {'pauseDEBUG':2, 'pauseINFO':3,
                                     'pauseWARN':4, 'pauseERROR':5,
                                     'pauseFATAL':6, 'pauseTARGET':7}

        for key,value in self.overridenLevelPauses.iteritems():
            self.configfh.write(key +'='+str(value)+'\n')
        self.configfh.close()
    
    def testgetDefaultPauseModeLevels(self):
        pauseMode = PauseMode()
        self.assertEqual(0,pauseMode.getPause('DEBUG'))
        self.assertEqual(0,pauseMode.getPause('INFO'))
        self.assertEqual(2,pauseMode.getPause('WARN'))
        self.assertEqual(3,pauseMode.getPause('ERROR'))
        self.assertEqual(5,pauseMode.getPause('FATAL'))
        self.assertEqual(5,pauseMode.getPause('TARGET'))

    def testgetOverridePauseModeLevels(self):
        pauseMode = PauseMode()
        properties = Property(self.configfile)
        properties.parseProperties()
        pauseMode.parseConfig(properties)
        for key,value in self.overridenLevelPauses.iteritems():
            key = key.split('pause')[1]
            self.assertEqual(value,pauseMode.getPause(key))
    
    def tearDown(self):
        os.remove(self.configfile)

if __name__=='__main__':
    unittest.main()





