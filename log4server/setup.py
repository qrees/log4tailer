from setuptools import setup, find_packages

__version__ = '0.1'

long_description = """
Log4server is a web backend application that receives notifications from
log4tailer clients, notifying in a web front page about the status of the logs
in several machines.  The clients will register first to the server and then
notify it if any fatal, error, critical or target logtrace has been found.
""" 


setup(name = "log4server",
      version = __version__ ,
      url = "http://bitbucket.org/jordilin/alerta",
      license = "GNU GPL v3",
      description = "log4tailer's server side",
      long_description = long_description,
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

