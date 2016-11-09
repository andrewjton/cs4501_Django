from django.test import TestCase, Client
from django.core.urlresolvers import reverse
import json
from django.utils import timezone
import experience.views
from django.forms.models import model_to_dict
from django.contrib.auth import hashers

class SearchTest(TestCase):

	def setUp(self):
		response = self.client.post('http://exp-api:8000/api/v1/job/n/', data={'price': 11, \
                                                                            'auth': 'auth', \
                                                                           'location': 'location', \
                                                                           'name': 'name', \
                                                                           'description': 'description'})
	def test_search(self):
		#must make POST request
		response = self.client.get('/api/v1/search/')
		self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "must make POST request")
		
		#token not found
		response = self.client.post('/api/v1/search/', data={"search":'word'})
		self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "no index created")
	
		#success
		#response = self.client.post('/api/v1/search/', data={"search":'location'})
		#self.assertEqual(json.loads(response.content.decode('utf8'))['ok'], True)
	
	def tearDown(self):
		pass