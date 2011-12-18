import os
from . import logcolors

class DefaultConfig(object):
    def __init__(self):
        self.actions = []
        self.pause = 1
        self.silence = False
        self.throttle = 0
        self.nlines = False
        self.target = None
        self.logcolors = logcolors.LogColors()
        self.properties = None
        self.alt_config = os.path.expanduser('~/.log4tailer')
        self.post = False
