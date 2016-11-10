from django.test import TestCase, Client
from django.core.urlresolvers import reverse
import json
from django.utils import timezone
import experience.views
from django.forms.models import model_to_dict
from django.contrib.auth import hashers
import requests

class SearchTest(TestCase):

	def setUp(self):
		
		request = requests.post('http://models-api:8000/api/v1/auth/n/', data={'user_id': 'user1'}).json()
		if request['ok']:
			token = request['resp']
			response = self.client.post('/api/v1/job/n/', data={'price': 11, \
                                                                            'auth': token, \
                                                                           'location': 'location', \
                                                                           'name': 'name', \
                                                                           'description': 'description'})
	def test_search(self):
		#must make POST request
		response = self.client.get('/api/v1/search/', data={"search":'word'})
		self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "must make POST request")
		
		#no search query
		response = self.client.post('/api/v1/search/')
		self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "no query string")
		
		#no results
		response = self.client.post('/api/v1/search/', data={"search":'word'})
		self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "No results found")
	
		#success
		response = self.client.post('/api/v1/search/', data={"search":'name'})
		self.assertEqual(json.loads(response.content.decode('utf8'))['ok'], True)
	
	def tearDown(self):
		pass