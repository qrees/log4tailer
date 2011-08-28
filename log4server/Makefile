PYTHON = python
BUILDOUT = bin/buildout
EXE = bin/log4server
ENV = ENV 
ENV24 = ENV24

all: $(BUILDOUT) $(EXE) 

env: $(ENV)

$(ENV):
	virtualenv --no-site-packages $(ENV)

env24: $(ENV24)

$(ENV24):
	virtualenv --no-site-packages --python=python2.4 $(ENV24)

runtests: $(TEST)
	$(TEST) -v --with-xunit 

coverage: $(TEST)
	$(TEST) -v --with-coverage --cover-package=log4tailer 

$(EXE): $(BUILDOUT) 
	$(BUILDOUT) install django

$(BUILDOUT): bootstrap.py
	$(PYTHON) bootstrap.py

# just sdist
release: $(EXE)
	$(PYTHON) setup.py release

# sdist and tag into subversion
releasetag: $(EXE)
	$(PYTHON) setup.py release --rtag

clean:
	@echo "clean ..."
	rm -f `find src -name "*.pyc"`
	rm -f `find tests -name "*.pyc"`
	rm -rf cover .coverage

distclean:
	@echo "distclean ..."
	rm -rf build dist bin 
	rm -f `find src -name "*.pyc"`
	rm -f `find tests -name "*.pyc"`
	rm -rf cover .coverage
	rm -rf develop-eggs
	rm -rf parts


