PYTHON = python
BUILDOUT = bin/buildout
EXE = bin/log4tail
TEST = bin/test

all: $(BUILDOUT) $(EXE) $(TEST)

runtests: $(TEST)
	$(TEST) 

coverage: $(TEST)
	$(TEST) -v --with-coverage --cover-package=log4tailer --cover-html

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
	rm -rf $(EXE) 
	rm -f `find . -name "*.pyc"`
	rm -rf cover .coverage

distclean:
	@echo "distclean ..."
	rm -rf build dist bin parts downloads develop-eggs eggs
	rm -rf .installed.cfg 
	rm -rf `find . -name "*.egg-info"`
	




