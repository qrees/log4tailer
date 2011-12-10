#!/usr/bin/env python

import unittest
from log4tailer import notifications
from tests import TESTS_DIR
import mocker
from mocker import ANY
from subprocess import PIPE
from log4tailer.message import Message
from log4tailer.LogColors import LogColors
from log4tailer.logfile import Log
import sys
import os
from os.path import join as pjoin
from tests import TESTS_DIR

CONFIG = 'printshot.cfg'

class Writer:
    def __init__(self):
        self.captured = []

    def __len__(self):
        return len(self.captured)

    def write(self, txt):
        self.captured.append(txt)

class PrintShotTest(unittest.TestCase):
    def setUp(self):
        self.mocker = mocker.Mocker()
        self.sysout = sys.stdout
        self.output = pjoin(TESTS_DIR, 'apicture.png')

    def test_instantiatesprintshot(self):
        output = 'picture.png'
        propertiesmock = self.mocker.mock()
        propertiesmock.get_value('screenshot')
        self.mocker.result(output)
        propertiesmock.get_value(ANY)
        self.mocker.result(False)
        self.mocker.replay()
        printshot = notifications.PrintShot(propertiesmock)
        self.assertTrue(isinstance(printshot, notifications.PrintShot))
        self.assertTrue(output, printshot.screenshot)

    def test_getwindowid(self):
        getId = "xprop -root | grep '_NET_ACTIVE_WINDOW(WINDOW)'"
        res = "_NET_ACTIVE_WINDOW(WINDOW): window id # 0x3a00004"
        winid = 0x3a00004
        procins = self.mocker.mock()
        procins.communicate()
        self.mocker.result((res, False))
        self.procmock = self.mocker.replace('subprocess')
        self.procmock.Popen(getId, shell = True, stdout = PIPE, stderr = PIPE)
        self.mocker.result(procins)
        output = 'picture.png'
        propertiesmock = self.mocker.mock()
        propertiesmock.get_value('screenshot')
        self.mocker.result(output)
        propertiesmock.get_value(ANY)
        self.mocker.result(False)
        self.mocker.replay()
        printshot = notifications.PrintShot(propertiesmock)
        self.assertTrue(0x3a00004, printshot.winid)

    def test_printandshoot(self):
        sys.stdout = Writer()
        log_traces = ['this is an info log trace',
                'this is a fatal log trace']
        log = Log('anylog')
        logcolors = LogColors()
        output = 'picture.png'
        propertiesmock = self.mocker.mock()
        propertiesmock.get_value('screenshot')
        self.mocker.result(output)
        propertiesmock.get_value(ANY)
        self.mocker.result(False)
        self.mocker.replay()
        printandshoot = notifications.PrintShot(propertiesmock,
                shot_process=pjoin(TESTS_DIR,"printashot.sh"))
        message = Message(logcolors)
        for trace in log_traces:
            message.parse(trace, log)
            printandshoot.notify(message, log)
        found = False
        for msg in sys.stdout.captured:
            if msg.find(log_traces[1]) >= 0:
                found = True
        if not found:
            self.fail()
        self.assertTrue(os.path.exists(self.output))

    def tearDown(self):
        if os.path.exists(self.output):
            os.remove(self.output)
        self.mocker.restore()
        self.mocker.verify()
        sys.stdout = self.sysout

if __name__ == '__main__':
    unittest.main()

