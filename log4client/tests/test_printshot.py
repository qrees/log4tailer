#!/usr/bin/env python

import unittest
from log4tailer import notifications
from log4tailer.message import Message
from log4tailer.logcolors import LogColors
from log4tailer.logfile import Log
import sys
from .utils import MemoryWriter
from .utils import SubProcessStub
from .utils import SubProcessStubRaise


def callback():
    pass


class PropertiesStub(object):

    def __init__(self):
        pass

    def get_value(self, value):
        if value == "screenshot":
            return "picture.png"


class ProcessStub(object):
    def __init__(self, returns_val):
        self.returns_val = returns_val

    def communicate(self):
        return (self.returns_val, None)


class ProcessStubErr(ProcessStub):
    msg = "boo, an error..."
    def communicate(self):
        return (self.returns_val, self.msg)


class SubProcessStubPopen(SubProcessStub):
    returns_val = "_NET_ACTIVE_WINDOW(WINDOW): window id # 0x3a00004"

    def __init__(self):
        pass

    @staticmethod
    def Popen(*args, **kwargs):
        return ProcessStub(SubProcessStubPopen.returns_val)


class SubProcessStubPopenProcErr(SubProcessStubPopen):

    @staticmethod
    def Popen(*args, **kwargs):
        return ProcessStubErr(SubProcessStubPopen.returns_val)


class PrintShotTest(unittest.TestCase):
    def setUp(self):
        self.sysout = sys.stdout
        sys.stdout = MemoryWriter()

    def test_instantiatesprintshot(self):
        def windowid(caller):
            return 345
        notifications.get_windowsid = windowid
        printshot = notifications.PrintShot(PropertiesStub())
        self.assertTrue(isinstance(printshot, notifications.PrintShot))

    def test_getwindowid(self):
        getId = "xprop -root | grep '_NET_ACTIVE_WINDOW(WINDOW)'"
        res = "_NET_ACTIVE_WINDOW(WINDOW): window id # 0x3a00004"
        expected_winid = "0x3a00004"
        caller = SubProcessStubPopen()
        winid = notifications.get_windowsid(caller)
        self.assertEqual(expected_winid, winid)

    def test_getwindowid_throws(self):
        getId = "xprop -root | grep '_NET_ACTIVE_WINDOW(WINDOW)'"
        res = "_NET_ACTIVE_WINDOW(WINDOW): window id # 0x3a00004"
        expected_winid = "0x3a00004"
        caller = SubProcessStubRaise()
        try:
            notifications.get_windowsid(caller)
            self.fail()
        except Exception:
            pass

    def test_getwindowid_error_process(self):
        getId = "xprop -root | grep '_NET_ACTIVE_WINDOW(WINDOW)'"
        res = "_NET_ACTIVE_WINDOW(WINDOW): window id # 0x3a00004"
        expected_winid = "0x3a00004"
        caller = SubProcessStubPopenProcErr()
        try:
            notifications.get_windowsid(caller)
            self.fail()
        except Exception, err:
            self.assertEqual(str(err), ProcessStubErr.msg)

    def test_printandshoot(self):
        log_trace = 'this is a fatal log trace'
        log = Log('anylog')
        logcolors = LogColors()
        caller = SubProcessStubPopen()
        printandshoot = notifications.PrintShot(PropertiesStub(),
                caller=caller)
        message = Message(logcolors)
        message.parse(log_trace, log)
        printandshoot.notify(message, log)
        colorized_logtrace = '\x1b[31mthis is a fatal log trace\x1b[0m'
        self.assertEqual(colorized_logtrace, sys.stdout.captured[0])
        # in [1] has '\n', and [2] should have the result
        self.assertEqual(SubProcessStub.msg, sys.stdout.captured[2])

    def test_printandshoot_notalertable(self):
        log_trace = 'this is an info log trace'
        log = Log('anylog')
        logcolors = LogColors()
        caller = SubProcessStubPopen()
        printandshoot = notifications.PrintShot(PropertiesStub(),
                caller=caller)
        message = Message(logcolors)
        message.parse(log_trace, log)
        printandshoot.notify(message, log)
        self.assertFalse(sys.stdout.contains(SubProcessStubPopen.msg))

    def test_printandshoot_throws(self):
        log_trace = 'this is a very fatal log trace'
        log = Log('anylog')
        logcolors = LogColors()
        caller = SubProcessStubRaise()
        printandshoot = notifications.PrintShot(PropertiesStub(),
                caller=caller)
        message = Message(logcolors)
        message.parse(log_trace, log)
        try:
            printandshoot.notify(message, log)
            self.fail()
        except Exception, err:
            self.assertEqual(str(err), SubProcessStubRaise.msg)


    def tearDown(self):
        sys.stdout = self.sysout
