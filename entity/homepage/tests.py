from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from homepage.models import User, Job
import json
from django.utils import timezone
import homepage.views
from django.forms.models import model_to_dict
from django.contrib.auth import hashers


class UserAPITest(TestCase):
    def setUp(self):
        User.objects.create(username='username',                         
                     first_name='first name',                            
                     last_name='last name',
                     date_created = timezone.now(),
                     dob= timezone.now(),
                     id = 1)


    def test_get_user(self, username='username'):
        
        #must make GET request
        response = self.client.post('/api/v1/user/'+str(username)+'/', {})
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "must make GET request")
        
        #user not found
        response = self.client.get('/api/v1/user/10000/')
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "user not found")
        #success
        response = self.client.get('/api/v1/user/'+str(username)+'/') 
        self.assertEqual(json.loads(response.content.decode('utf8'))['ok'], True)    
    

    def test_get_all_users(self):
        #must make GET request
        response = self.client.post('/api/v1/user/all/', {})
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "must make GET request")
        
        #success
        response = self.client.get('/api/v1/user/all/')
        self.assertEqual(json.loads(response.content.decode('utf8'))['ok'], True)

    def test_update_user(self, user_id=1):
        #must make POST request
        response = self.client.get('/api/v1/user/u/')
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "must make POST request")
        
        #user not found
        response = self.client.post('/api/v1/user/u/', {"user_id" : 1000000})
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "user not found")
        
        #no fields updated
        response = self.client.post('/api/v1/user/u/', {"user_id" : user_id})
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], 'no fields updated')
        
        #success
        response = self.client.post('/api/v1/user/u/', {'user_id' : user_id, 'first_name' : 'New First Name'})
        self.assertEqual(json.loads(response.content.decode('utf8'))['ok'], True)
    
    def test_delete_user(self, username='username'):
        #must make POST request
        response = self.client.get('/api/v1/user/d/')
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "must make POST request")
        
        #invalid request parameters
        response = self.client.post('/api/v1/user/d/', {'user_id' : 10000})
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "invalid request parameters")

        #success
        response = self.client.post('/api/v1/user/d/', {'username' : username})
        self.assertEqual(json.loads(response.content.decode('utf8'))['ok'], True)
        
    def test_create_user(self):
        #must make POST request
        response = self.client.get('/api/v1/user/n/')
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'] , "must make POST request")
        
        # missing required fields
        response = self.client.post('/api/v1/user/n/', {'username' : 'user1', \
                                                         'first_name' : 'first_name', \
                                                         'dob' : timezone.now()})
        
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "missing required fields")
         
        #successful creation
        response = self.client.post('/api/v1/user/n/', {'username' : 'user1', \
                                                        'password' : hashers.make_password('password'), \
                                                         'first_name' : 'first_name', \
                                                         'last_name' : 'last_name', \
                                                         'dob' : timezone.now()})
        self.assertEqual(json.loads(response.content.decode('utf8'))['ok'], True)

    def tearDown(self):
        pass





class TestJobAPI(TestCase):
    def setUp(self):
        User.objects.create(username='username',                         
                      first_name='first name',                            
                      last_name='last name',
                      date_created = timezone.now(),
                      dob= timezone.now(),
                      id = 1)
        
        Job.objects.create(name='name',                         
                     description='description',                            
                     location='somewhere',                             
                     price= 5.0,  
                     taken = False,
                     date_created = timezone.now(),
                     cleaner = User.objects.get(pk=1),
                     owner = User.objects.get(pk=1),
                     id = 1) 
        
    def test_create_job(self):
        #TODO: check for 'ok' or resp value??
        
        #must make POST request
        response = self.client.get('/api/v1/job/n/')
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'] , "must make POST request")
        
        # missing required fields
        response = self.client.post('/api/v1/job/n/', {'name' : 'job1', \
                                                         'description' : 'test job', \
                                                         'location' : 'somewhere'})
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "missing required fields")
        
        #DB creation error
        response = self.client.post('/api/v1/job/n/', {'name' : 'job1', \
                                                         'location' : 'somewhere', \
                                                         'description' : 6, \
                                                         'price' : "5", \
                                                         'date_created' : "2016-10-27", \
                                                         'cleaner' : "", \
                                                         'owner' : ""})  
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "DB creation error")
        
        #successful creation
        response = self.client.post('/api/v1/job/n/', {'name' : 'job1', \
                                                         'location' : 'somewhere', \
                                                         'description' : 'test job', \
                                                         'price' : 5.0, \
                                                         'date_created' : "2016-10-27", \
                                                         'cleaner' : User.objects.get(pk=1), \
                                                         'owner' : User.objects.get(pk=1)})
        self.assertEqual(json.loads(response.content.decode('utf8'))['ok'], True) 

    def test_get_job(self, job_id=1):
        #must make GET request
        response = self.client.post('/api/v1/job/'+str(job_id)+'/', {})
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "must make GET request")
        
        #job not found
        response = self.client.get('/api/v1/job/10000/')
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "job not found")
        
        #success provided db has the job
        response = self.client.get('/api/v1/job/'+str(job_id)+'/')
        self.assertEqual(json.loads(response.content.decode('utf8'))['ok'], True)
        
    def test_update_job(self, job_id=1):
        #must make POST request
        response = self.client.get('/api/v1/job/u/')
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "must make POST request")
        
        #job not found
        response = self.client.post('/api/v1/job/u/', {'job_id' : 1000})
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "job not found")
        
        #no fields updated
        response = self.client.post('/api/v1/job/u/', {'job_id' : job_id})
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], 'no fields updated')
        
        #success
        response = self.client.post('/api/v1/job/u/', {'job_id' : job_id, 'description' : 'New Description'})
        self.assertEqual(json.loads(response.content.decode('utf8'))['ok'], True)
            
        
    def test_get_all_jobs(self):
        #must make GET request
        response = self.client.post('/api/v1/job/all/', {})
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "must make GET request")
        
        #What condition would this fail under? No db?
        
        #success
        response = self.client.get('/api/v1/job/all/')
        self.assertEqual(json.loads(response.content.decode('utf8'))['ok'], True)
    def test_delete_job(self, job_id=1):
        #must make POST request
        response = self.client.get('/api/v1/job/d/')
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "must make POST request")
        
        #invalid request parameters
        response = self.client.post('/api/v1/job/d/', {'job_id' : 10000})
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "invalid request parameters")

        #success
        response = self.client.post('/api/v1/job/d/', {'job_id' : job_id})
        self.assertEqual(json.loads(response.content.decode('utf8'))['ok'], True)
        

    def tearDown(self):
        pass




