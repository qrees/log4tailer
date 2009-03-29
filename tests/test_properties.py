import unittest
import os,sys

sys.path.append('..')
from log4tailer.Properties import Property

class TestProperties(unittest.TestCase):
    def setUp(self):
        self.configfile = 'config.txt'
        self.configfh = open(self.configfile,'w')
        colorconfigs = {'warn':'yellow','fatal':'red',
                        'error':'red'}
        for key,value in colorconfigs.iteritems():
            self.configfh.write(key +'='+value+'\n')
        self.configfh.close()
        self.configKeys = colorconfigs.keys().sort()

    def test_parseProperties(self):
        property = Property(self.configfile)
        property.parseProperties()
        configPropertyKeys = property.getKeysLower().sort()
        # my colorconfigs keys are already in lowercase
        self.assertEqual(self.configKeys,configPropertyKeys)
        


    def tearDown(self):
        os.remove(self.configfile)



if __name__=='__main__':
    unittest.main()





