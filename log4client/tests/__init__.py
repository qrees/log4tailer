import copy
import log4tailer
from os.path import abspath, dirname

TESTS_DIR = dirname(abspath(__file__))
LOG4TAILER_DEFAULTS = copy.deepcopy(log4tailer.defaults)

