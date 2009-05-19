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


long_description = '''
Introduction
============
This project aims to provide a different approach to traditional log tailers.
Amongst other features:

* Multitailing capability. It can tail multiple logs at a time
* Colors for every level: warn, info, debug, error and fatal
* Emphasize multiple targets (log traces) given regular expressions
* Follow log upon truncation by default
* User defined colors for each level
* Silent (daemonized) mode
* Throttling mode. Slow down the information being printed in the terminal
* Inactivity log monitoring
* mail notification
* Pause Modes freezes output for a limited period of time depending on level found.
* Analytics. Makes a report of each level found in logs when finished. 

Why yet another tailer?
=======================
Most people use tail -F to tail the logs these days. When debugging enterprise
class applications you cannot just follow (in many situations) what is going on
unless you go to the log, less it and check if something was wrong, or just
Ctrl-C tail program and scroll back. Human eye cannot distinguish or grab a
line out of thousands when that information is showed incredibly fast in the
screen. By providing colors, the human eye will discern and quickly identify
specific levels or lines. 
'''

__version__='1.4'

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
        for i in range(2):
            # compile two times to fix cross references
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
    user_options = [('rtag',None,"definitive version, tag and release")]

    def initialize_options(self):
        self.rtag = False
    
    def finalize_options(self):
        pass

    def run(self):
        # check everything is ok
        if self.rtag:
            # push release to svn 
            # and tag it with release version
            httpcurrdir = 'https://log4tailer.googlecode.com/svn/trunk/'
            httpdestdir = 'https://log4tailer.googlecode.com/svn/tags/log4tailer-'+__version__
            releasecomment = "Log4Tailer release version "+__version__
            svncommand = ['svn','copy',httpcurrdir,httpdestdir,'-m',releasecomment]
            svnproc = Popen(svncommand,stdout = PIPE)
            print "tagging project into googlecode svn"
            out,err = svnproc.communicate()
            print out
        
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
      long_description = long_description,
      author="Jordi Carrillo",
      author_email = "jordilin@gmail.com",
      url = "http://code.google.com/p/log4tailer/",
      license = "GNU GPL v3",
      packages=["log4tailer"] + map("log4tailer.".__add__,PACKAGES),
      scripts = ["log4tail"],
      cmdclass = {"release":Release,"test":Test, "clean":Clean,"dodoc":DoDoc},
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: System :: Monitoring'
          ],
      )
