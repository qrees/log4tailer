import unittest
import os,sys

sys.path.append('..')
from log4tailer.Properties import Property
from log4tailer.log4Exceptions import KeyAlreadyExistsException,KeyNotFoundException

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

    def testparseProperties(self):
        property = Property(self.configfile)
        property.parseProperties()
        configPropertyKeys = property.getKeysLower().sort()
        # my colorconfigs keys are already in lowercase
        self.assertEqual(self.configKeys,configPropertyKeys)
    
    def testKeyNotfoundException(self):
        property = Property(self.configfile)
        property.parseProperties()
        key = 'hi'
        self.assertRaises(KeyNotFoundException,property.getValue,key)
    
    def __createDuplicateKeysConfig(self):
        os.remove(self.configfile)
        configfh = open(self.configfile,'w')
        colorconfigs = {'warn':'yellow','fatal':'red','error':'red'}
        for key,value in colorconfigs.iteritems():
            configfh.write(key +'='+value+'\n')
        # making a duplicate level
        configfh.write('warn'+'='+'red'+'\n')
        configfh.close()

    def testKeyAlreadyExistsException(self):
        self.__createDuplicateKeysConfig()
        property = Property(self.configfile)
        self.assertRaises(KeyAlreadyExistsException,property.parseProperties)

    def tearDown(self):
        os.remove(self.configfile)



if __name__=='__main__':
    unittest.main()





