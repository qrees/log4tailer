PYTHON = python
BUILDOUT = bin/buildout
EXE = bin/log4tail
TEST = bin/test
ENV = ENV 
ENV24 = ENV24

all: $(BUILDOUT) $(EXE) $(TEST)

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
	$(BUILDOUT) install log4tail

$(BUILDOUT): bootstrap.py
	$(PYTHON) bootstrap.py

# just sdist
release: $(EXE)
	$(PYTHON) setup.py release

# sdist and tag into subversion
releasetag: $(EXE)
	$(PYTHON) setup.py release --rtag

$(TEST): $(BUILDOUT)
	$(BUILDOUT) install test

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


