from django.test import TestCase
from django.test import Client
from log4server.logs.models import Log

class Alerta(TestCase):
    def setUp(self):
        self.client = Client()

    def test_adeu_addition(self):
        params = {'logtrace' : 'fatal alert here',
                'logpath' : '/var/log/out.log'}
        response = self.client.post('/alerts/', params)
        self.assertEqual(201, response.status_code)

    def test_trae_saved(self):
        params = {'logtrace' : 'fatal alert here',
                'logpath' : '/var/log/out.log'}
        response = self.client.post('/alerts/', params)
        self.assertEqual(201, response.status_code)
        logs = Log.objects.all()
        self.assertEqual(1, len(logs))

    def test_gt_alerts(self):
        pass




