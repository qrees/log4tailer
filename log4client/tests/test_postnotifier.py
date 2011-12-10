#!/usr/bin/env python

import unittest
import mocker
from log4tailer import notifications
from log4tailer.LogColors import LogColors
from log4tailer.message import Message
from log4tailer.Log import Log
import json

def mock_server(mocker_obj):
    body = json.dumps({'status_code' : 200})
    response = mocker_obj.mock()
    response.read()
    mocker_obj.count(1, 2)
    mocker_obj.result(body)
    conn = mocker_obj.mock()
    conn.request(mocker.ARGS)
    mocker_obj.count(1, 2)
    conn.getresponse()
    mocker_obj.count(1, 2)
    mocker_obj.result(response)
    conn.close()
    mocker_obj.count(1, 2)
    httpconn_mock = mocker_obj.replace('httplib')
    httpconn_mock.HTTPConnection(mocker.ANY, mocker.ANY)
    mocker_obj.count(1, 2)
    mocker_obj.result(conn)


class TestPost(unittest.TestCase):
    def setUp(self):
        self.mocker = mocker.Mocker()

    def test_post_notification(self):
        properties = self.mocker.mock()
        properties.get_value('server_url')
        self.mocker.result('localhost')
        properties.get_value('server_port')
        self.mocker.result(8000)
        properties.get_value('server_service_uri')
        self.mocker.result('/')
        properties.get_value('server_service_register_uri')
        self.mocker.result('/register')
        properties.get_value('server_service_unregister_uri')
        self.mocker.result('/unregister')
        self.mocker.replay()
        poster = notifications.Poster(properties)
        self.assertTrue(isinstance(poster, notifications.Poster))

    def test_has_notify_method(self):
        properties = self.mocker.mock()
        properties.get_value('server_url')
        self.mocker.result('localhost')
        properties.get_value('server_port')
        self.mocker.result(8000)
        properties.get_value('server_service_uri')
        self.mocker.result('/')
        properties.get_value('server_service_register_uri')
        self.mocker.result('/register')
        properties.get_value('server_service_unregister_uri')
        self.mocker.result('/unregister')
        self.mocker.replay()
        poster = notifications.Poster(properties)
        self.assertTrue(getattr(poster, 'notify'))

    def test_shouldPost_if_alertable(self):
        properties = self.mocker.mock()
        properties.get_value('server_url')
        self.mocker.result('localhost')
        properties.get_value('server_port')
        self.mocker.result(8000)
        properties.get_value('server_service_uri')
        self.mocker.result('/')
        properties.get_value('server_service_register_uri')
        self.mocker.result('/register')
        properties.get_value('server_service_unregister_uri')
        self.mocker.result('/unregister')
        logcolors = LogColors()
        logtrace = 'this is an error log trace'
        log = Log('anylog')
        message = Message(logcolors)
        message.parse(logtrace, log)
        mock_server(self.mocker)
        self.mocker.replay()
        poster = notifications.Poster(properties)
        body = poster.notify(message, log)
        self.assertTrue(body)

    def test_execute_if_targetMessage(self):
        properties = self.mocker.mock()
        properties.get_value('server_url')
        self.mocker.result('localhost')
        properties.get_value('server_port')
        self.mocker.result(8000)
        properties.get_value('server_service_uri')
        self.mocker.result('/')
        properties.get_value('server_service_register_uri')
        self.mocker.result('/register')
        properties.get_value('server_service_unregister_uri')
        self.mocker.result('/unregister')
        logcolors = LogColors()
        logtrace = 'this is a target log trace'
        log = Log('anylog')
        message = Message(logcolors, target = 'trace')
        message.parse(logtrace, log)
        mock_server(self.mocker)
        self.mocker.replay()
        poster = notifications.Poster(properties)
        body = poster.notify(message, log)
        self.assertTrue(body)

    def test_not_execute_if_not_alertable_Level(self):
        properties = self.mocker.mock()
        properties.get_value('server_url')
        self.mocker.result('localhost')
        properties.get_value('server_port')
        self.mocker.result(8000)
        properties.get_value('server_service_uri')
        self.mocker.result('/')
        properties.get_value('server_service_register_uri')
        self.mocker.result('/register')
        properties.get_value('server_service_unregister_uri')
        self.mocker.result('/unregister')
        logcolors = LogColors()
        logtrace = 'this is an info log trace'
        log = Log('anylog')
        message = Message(logcolors, target = 'anything')
        message.parse(logtrace, log)
        self.mocker.replay()
        poster = notifications.Poster(properties)
        poster.registered_logs[log] = True
        body = poster.notify(message, log)
        self.assertFalse(body)

    def test_register_to_server_first_time(self):
        properties = self.mocker.mock()
        properties.get_value('server_url')
        self.mocker.result('localhost')
        properties.get_value('server_port')
        self.mocker.result(8000)
        properties.get_value('server_service_uri')
        self.mocker.result('/')
        properties.get_value('server_service_register_uri')
        self.mocker.result('/register')
        properties.get_value('server_service_unregister_uri')
        self.mocker.result('/unregister')
        logcolors = LogColors()
        log = Log('anylog')
        mock_server(self.mocker)
        self.mocker.replay()
        poster = notifications.Poster(properties)
        body = poster.register(log)
        self.assertFalse(body)

    def test_unregister_method_for_shutdown(self):
        properties = self.mocker.mock()
        properties.get_value('server_url')
        self.mocker.result('localhost')
        properties.get_value('server_port')
        self.mocker.result(8000)
        properties.get_value('server_service_uri')
        self.mocker.result('/')
        properties.get_value('server_service_register_uri')
        self.mocker.result('/register')
        properties.get_value('server_service_unregister_uri')
        self.mocker.result('/unregister')
        logcolors = LogColors()
        log = Log('anylog')
        mock_server(self.mocker)
        self.mocker.replay()
        poster = notifications.Poster(properties)
        poster.registered_logs[log] = {'id' : 5, 'logserver' : 'anyserver'}
        body = poster.unregister(log)
        self.assertTrue(body)

    def tearDown(self):
        self.mocker.restore()
        self.mocker.verify()

