from distutils.core import setup

PACKAGES = ("Actions Analytics").split()

setup(name="log4tailer",
      version="1.0",
      description="Not just a simple log tailer",
      author="Jordi Carrillo",
      author_email = "jordilin@gmail.com",
      url = "http://code.google.com/p/log4tailer/",
      license = "GNU GPL v3",
      packages=["log4tailer"] + map("log4tailer.".__add__,PACKAGES),
      scripts = ["log4tail"])
