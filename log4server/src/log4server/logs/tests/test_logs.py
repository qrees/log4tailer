from django.test import TestCase
from django.test import Client
from log4server.logs.models import Log

class AlertTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_postalert(self):
        params = {'logtrace' : 'fatal alert here',
                'logpath' : '/var/log/out.log'}
        response = self.client.post('/alerts/', params)
        self.assertEqual(201, response.status_code)

    def test_alert_saved(self):
        params = {'logtrace' : 'fatal alert here',
                'logpath' : '/var/log/out.log'}
        response = self.client.post('/alerts/', params)
        self.assertEqual(201, response.status_code)
        logs = Log.objects.all()
        self.assertEqual(1, len(logs))

    def test_notenoughinfo_alerts(self):
        params = {'logpath' : '/var/log/out.log'}
        response = self.client.post('/alerts/', params)
        self.assertEqual(404, response.status_code)

    def test_noGET_alerts(self):
        response = self.client.get('/alerts/')
        self.assertEqual(404, response.status_code)

    def test_info_alerts(self):
        response = self.client.get('/alerts/info/')
        self.assertEqual(200, response.status_code)
 
 

