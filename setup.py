# Log4Tailer: A multicolored python tailer for log4J logs
# Copyright (C) 2008 Jordi Carrillo Bosch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys 

from distutils.core import Command
from unittest import TextTestRunner, TestLoader
from glob import glob
from os.path import splitext, basename, join as pjoin, walk
from subprocess import Popen,PIPE
import os,shutil

__version__='1.2'

try:
    from distutils.core import setup
except:
    print "You need to install distutils python module"
    sys.exit()
    
class Test(Command):
    user_options = []

    def initialize_options(self):
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run(self):
        '''Finds all the tests modules in test/, and runs them.
        '''
        testfiles = []
        for t in glob(pjoin(self._dir, 'test', '*.py')):
            if not t.endswith('__init__.py'):
                testfiles.append('.'.join(
                    ['test', splitext(basename(t))[0]])
                )
        tests = TestLoader().loadTestsFromNames(testfiles)
        t = TextTestRunner(verbosity = 2)
        t.run(tests)


class DoDoc(Command):
    user_options = []

    def initialize_options(self):
        # if you're not Jordi, I guess
        # this is not gonna work for you
        if not os.path.isdir('../userguide/'):
            print "checkout userguide"
            sys.exit()
    
    def finalize_options(self):
        pass

    def run(self):
        destdir = pjoin(os.getcwd(),"dist")
        if not os.path.isdir(destdir):
            print "making distribution dir"
            os.mkdir(destdir)
        os.chdir('../userguide')
        pdfexec = 'pdflatex'
        file = 'log4tailer.tex'
        destfile = pjoin(destdir,'UserGuide-'+__version__+'.pdf')
        docproc = Popen([pdfexec,file],stdout=PIPE)
        out,err = docproc.communicate()
        print out
        shutil.copy('log4tailer.pdf',destfile)

class Clean(Command):
    user_options = []
    
    def initialize_options(self):
        self.__toRemove = []
        for root,path,files in os.walk("."):
            for file in files:
                if file.endswith(('~','pyc')):
                    self.__toRemove.append(os.path.join(root,file))
    
    def finalize_options(self):
        pass
    
    def run(self):
        curdir = os.getcwd()
        distdir = pjoin(curdir,"dist")
        if os.path.exists(distdir):
            print "removing distribution directory"
            shutil.rmtree(distdir)
        
        manifest = pjoin(curdir,'MANIFEST')
        if os.path.exists(manifest):
            print "removing MANIFEST file"
            os.unlink(manifest)

        for file in self.__toRemove:
            try:
                print "removing "+file
                os.unlink(file)
            except:
                pass

class Release(Command):
    user_options = []

    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass

    def run(self):
        # check everything is ok
        self.run_command("test")
        self.run_command("sdist")
        if not os.path.isdir('dist'):
            print "I just run sdist and no dist??"
            sys.exit()
        self.run_command("dodoc")



PACKAGES = ("Actions Analytics").split()

setup(name="log4tailer",
      version=__version__,
      description="Not just a simple log tailer",
      author="Jordi Carrillo",
      author_email = "jordilin@gmail.com",
      url = "http://code.google.com/p/log4tailer/",
      license = "GNU GPL v3",
      packages=["log4tailer"] + map("log4tailer.".__add__,PACKAGES),
      scripts = ["log4tail"],
      cmdclass = {"release":Release,"test":Test, "clean":Clean,"dodoc":DoDoc})
