#!/usr/bin/env python

import unittest
import mocker
import threading
from wsgiref.simple_server import make_server, demo_app
from log4tailer import notifications
from log4tailer.LogColors import LogColors
from log4tailer.Message import Message
from log4tailer.Log import Log
import sys
import decorators as dec

class ServerT(threading.Thread):
    def __init__(self, host = 'localhost', port = 8000):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.httpd = make_server(self.host, self.port, demo_app)
    
    def run(self):
        self.httpd.serve_forever()

    def stop(self):
        self.httpd.shutdown()
        self.join()

SERVER = None

def require_server():
    global SERVER
    if not SERVER:
        SERVER = ServerT()
        SERVER.start()

version_info = sys.version_info
version2_4 = (2, 4)
skip_from_time = False
if version_info[:2] == version2_4:
    skip_from_time = True


@dec.skipif(skip_from_time, "invalid for 2.4")
class TestPost(unittest.TestCase):
    def setUp(self):
        self.mocker = mocker.Mocker()
    
    def test_post_notification(self):
        properties = self.mocker.mock()
        properties.getValue('server_url')
        self.mocker.result('localhost')
        properties.getValue('server_port')
        self.mocker.result(8000)
        properties.getValue('server_service_uri')
        self.mocker.result('/')
        properties.getValue('server_service_register_uri')
        self.mocker.result('/register')
        properties.getValue('server_service_unregister_uri')
        self.mocker.result('/unregister')
        self.mocker.replay()
        poster = notifications.Poster(properties)
        self.assertTrue(isinstance(poster, notifications.Poster))

    def test_has_notify_method(self):
        properties = self.mocker.mock()
        properties.getValue('server_url')
        self.mocker.result('localhost')
        properties.getValue('server_port')
        self.mocker.result(8000)
        properties.getValue('server_service_uri')
        self.mocker.result('/')
        properties.getValue('server_service_register_uri')
        self.mocker.result('/register')
        properties.getValue('server_service_unregister_uri')
        self.mocker.result('/unregister')
        self.mocker.replay()
        poster = notifications.Poster(properties)
        self.assertTrue(getattr(poster, 'notify'))

    def test_shouldPost_if_alertable(self):
        properties = self.mocker.mock()
        properties.getValue('server_url')
        self.mocker.result('localhost')
        properties.getValue('server_port')
        self.mocker.result(8000)
        properties.getValue('server_service_uri')
        self.mocker.result('/')
        properties.getValue('server_service_register_uri')
        self.mocker.result('/register')
        properties.getValue('server_service_unregister_uri')
        self.mocker.result('/unregister')
        logcolors = LogColors()
        logtrace = 'this is an error log trace'
        log = Log('anylog')
        message = Message(logcolors)
        message.parse(logtrace, log)
        self.mocker.replay()
        poster = notifications.Poster(properties)
        require_server()
        response = poster.notify(message, log)
        self.assertEqual(response.status, 200)

    def test_execute_if_targetMessage(self):
        properties = self.mocker.mock()
        properties.getValue('server_url')
        self.mocker.result('localhost')
        properties.getValue('server_port')
        self.mocker.result(8000)
        properties.getValue('server_service_uri')
        self.mocker.result('/')
        properties.getValue('server_service_register_uri')
        self.mocker.result('/register')
        properties.getValue('server_service_unregister_uri')
        self.mocker.result('/unregister')
        logcolors = LogColors()
        logtrace = 'this is a target log trace'
        log = Log('anylog')
        message = Message(logcolors, target = 'trace')
        message.parse(logtrace, log)
        self.mocker.replay()
        poster = notifications.Poster(properties)
        require_server()
        response = poster.notify(message, log)
        self.assertEqual(response.status, 200)

    def test_not_execute_if_not_alertable_Level(self):
        properties = self.mocker.mock()
        properties.getValue('server_url')
        self.mocker.result('localhost')
        properties.getValue('server_port')
        self.mocker.result(8000)
        properties.getValue('server_service_uri')
        self.mocker.result('/')
        properties.getValue('server_service_register_uri')
        self.mocker.result('/register')
        properties.getValue('server_service_unregister_uri')
        self.mocker.result('/unregister')
        logcolors = LogColors()
        logtrace = 'this is an info log trace'
        log = Log('anylog')
        message = Message(logcolors, target = 'anything')
        message.parse(logtrace, log)
        self.mocker.replay()
        poster = notifications.Poster(properties)
        poster.registered = True
        response = poster.notify(message, log)
        self.assertFalse(response)

    def test_register_to_server_first_time(self):
        properties = self.mocker.mock()
        properties.getValue('server_url')
        self.mocker.result('localhost')
        properties.getValue('server_port')
        self.mocker.result(8000)
        properties.getValue('server_service_uri')
        self.mocker.result('/')
        properties.getValue('server_service_register_uri')
        self.mocker.result('/register')
        properties.getValue('server_service_unregister_uri')
        self.mocker.result('/unregister')
        logcolors = LogColors()
        log = Log('anylog')
        self.mocker.replay()
        require_server()
        poster = notifications.Poster(properties)
        response = poster.register(log)
        self.assertEqual(response.status, 200)

    def test_unregister_method_for_shutdown(self):
        properties = self.mocker.mock()
        properties.getValue('server_url')
        self.mocker.result('localhost')
        properties.getValue('server_port')
        self.mocker.result(8000)
        properties.getValue('server_service_uri')
        self.mocker.result('/')
        properties.getValue('server_service_register_uri')
        self.mocker.result('/register')
        properties.getValue('server_service_unregister_uri')
        self.mocker.result('/unregister')
        logcolors = LogColors()
        log = Log('anylog')
        self.mocker.replay()
        require_server()
        poster = notifications.Poster(properties)
        poster.registered = True
        response = poster.unregister(log)
        self.assertEqual(response.status, 200)

    def tearDown(self):
        self.mocker.restore()
        self.mocker.verify()
        global SERVER
        if SERVER:
            SERVER.stop()
            SERVER = None

if __name__ == '__main__':
    unittest.main()

