from django.test import TestCase
from django.test import Client
from django.utils import simplejson as json
from log4server.logs.models import Log, LogTrace
import urllib

JSON_STR = 'application/json'

class AlertTest(TestCase):
    fixtures = ['logs.json']

    def setUp(self):
        self.client = Client()

    def test_postalert(self):
        params = {'logtrace' : 'fatal alert here', 'loglevel' : 'fatal',
                'log' : {'id' : 1, 'logpath' : '/var/log/out.log',
                'logserver' : 'anyserver'}}
        response = self.client.post('/alerts/', json.dumps(params), JSON_STR)
        self.assertEqual(201, response.status_code)
        traces = LogTrace.objects.filter(logtrace__endswith = 'here', log__id =
                1).count()
        self.assertTrue(traces > 0)

    def test_alert_saved(self):
        params = {'logtrace' : 'fatal alert overthere', 'loglevel' : 'fatal',
                'log' : {'id' : 2, 'logpath' : '/var/log/out.log',
                'logserver' : 'anyserver'}}
        response = self.client.post('/alerts/', json.dumps(params), JSON_STR)
        self.assertEqual(201, response.status_code)
        traces = LogTrace.objects.filter(logtrace__endswith = 'overthere',
                log__id = 2).count()
        self.assertTrue(traces > 0)

    def test_notenoughinfo_alerts(self):
        params = {'log' : {'logpath' : '/var/log/out.log'}}
        response = self.client.post('/alerts/', json.dumps(params), JSON_STR)
        self.assertEqual(400, response.status_code)

    def test_nodata_alerts(self):
        params = {}
        response = self.client.post('/alerts/', json.dumps(params), JSON_STR)
        self.assertEqual(400, response.status_code)

    def test_noGET_alerts(self):
        response = self.client.get('/alerts/')
        self.assertEqual(404, response.status_code)

    def test_info_alerts(self):
        response = self.client.get('/alerts/status/')
        self.assertEqual(200, response.status_code)


class AlertNoInfoDB(TestCase):
    def test_no_info_db(self):
        params = {'logtrace' : 'fatal alert overthere', 'loglevel' : 'fatal',
                'log' : {'id' : 2, 'logpath' : '/var/log/out.log',
                'logserver' : 'anyserver'}}
        response = self.client.post('/alerts/', json.dumps(params), JSON_STR)
        self.assertEqual(404, response.status_code)

class LogRegisterDB(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_register_db(self):
        params = {'logpath' : '/var/log/out.log', 
                'logserver' : '192.168.1.2'}
        response = self.client.post('/register/', json.dumps(params), JSON_STR)
        self.assertEqual(201, response.status_code)


    def test_register_notenough_params(self):
        params = {'logpath' : '/var/log/out.log'}
        response = self.client.post('/register/', json.dumps(params), JSON_STR)
        self.assertEqual(400, response.status_code)
        
class SearchLogs(TestCase):
    fixtures = ['logs.json']
    
    def setUp(self):
        self.client = Client()
    
    def test_search(self):
        params = {'logtrace' : 'fatal alert here', 'loglevel' : 'fatal',
                'log' : {'id' : 1, 'logpath' : '/var/log/out.log',
                'logserver' : 'anyserver'}}
        response = self.client.post('/alerts/', json.dumps(params), JSON_STR)
        self.assertEqual(201, response.status_code)
 
        params = {'query' : 'fatal alert'}
        url = '/alerts/search/?' + urllib.urlencode(params)
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    #def test_showonly(self):
# 
        #params = {'query' : 'fatal alert'}
        #url = '/alerts/search/ComboN?' + urllib.urlencode(params)
        #response = self.client.get(url)
        #self.assertEqual(200, response.status_code)
#




