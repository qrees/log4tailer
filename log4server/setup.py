from setuptools import setup, find_packages

__version__ = '0.1'

setup(name = "log4server",
      version = __version__ ,
      url = "http://code.google.com/p/log4tailer/",
      license = "GNU GPL v3",
      description = "log4tailer's server side",
      author = 'Jordi Carrillo',
      author_email = 'jordilin@gmail.com',
      packages = find_packages('src'),
      package_dir = {'': 'src'},
      classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: POSIX',
            'Programming Language :: Python',
            'Topic :: System :: Monitoring'
        ])

