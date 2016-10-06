from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from homepage.models import User, Job
import datetime, json
import homepage.views


#TODO: need separate classes for each model?
class ModelTests(TestCase):
    def setUp(self):
        pass
    def runTest(self):
         user = User(username='username',                         
                    first_name='first name',                            
                    last_name='last name',                             
                    dob= datetime.datetime.now())
         self.assertTrue(isinstance(user, User))
         job = Job(name='name',                         
                    description='description',                            
                    location='somewhere',                             
                    price= 5.0,  
                    taken = False) #no owner 
         self.assertTrue(isinstance(job, Job))
    def tearDown(self):
        pass
    




class UserAPITest(TestCase):
    def setUp(self):
        self.c = Client()
    def create_user(self):
        #TODO: check for 'ok' or resp value??
        
        #must make POST request
        response = self.c.get('/homepage/api/user/n/')
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'] , "must make POST request")
        
        # missing required fields
        response = self.c.post('/homepage/api/user/n/', {'username' : 'user1', \
                                                         'first_name' : 'first_name', \
                                                         'dob' : datetime.datetime.now()})
        
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "missing required fields")
         
        #successful creation
        response = self.c.post('/homepage/api/user/n/', {'username' : 'user1', \
                                                         'first_name' : 'first_name', \
                                                         'last_name' : 'last_name', \
                                                         'dob' : datetime.datetime.now()})
        self.assertEqual(json.loads(response.content.decode('utf8'))['ok'], True) 

    def get_user(self, user_id):
        #must make GET request
        response = self.c.post('/homepage/api/user/'+str(user_id)+'/', {})
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "must make GET request")
        
        #user not found
        response = self.c.get('/homepage/api/user/10000/')
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "user not found")
        
        #success
        response = self.c.get('/homepage/api/user/'+str(user_id)+'/') 
        self.assertEqual(json.loads(response.content.decode('utf8'))['ok'], True) #will be false with db empty
       
    def get_all_users(self):
        #must make GET request
        response = self.c.post('/homepage/api/user/all/', {})
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "must make GET request")
        
        #What condition would this fail under? No db?
        
        #success
        response = self.c.get('/homepage/api/user/all/')
        self.assertEqual(json.loads(response.content.decode('utf8'))['ok'], True)
        
    def update_user(self, user_id):
        #must make POST request
        response = self.c.get('homepage/api/user/u/')
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "must make POST request")
        
        #user not found
        response = self.c.post('homepage/api/user/u/', {"user_id" : 1000000})
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "user not found")
        
        #no fields updated
        response = self.c.post('hompage/api/user/u/', {"user_id" : user_id})
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], 'no fields updated')
        
        #success
        response = self.c.post('homepage/api/user/u/', {'user_id' : user_id, 'first_name' : 'New First Name'})
        self.assertEqual(json.loads(response.content.decode('utf8'))['ok'], 'True')
    
    def delete_user(self, user_id):
        #must make POST request
        response = self.c.get('/homepage/api/user/d/')
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "must make POST request")
        
        #invalid request parameters
        response = self.c.post('/homepage/api/user/d/', {'user_id' : 10000})
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "invalid request parameters")

        #success
        response = self.c.post('/homepage/api/user/d/', {'user_id' : user_id})
        self.assertEqual(response['ok'], True)
        
    def runTest(self):
        self.create_user()
        self.get_user(1)
        self.get_all_users()
        self.update_user(1) 
        self.delete_user(1)
    def tearDown(self):
        pass




class TestJobAPI(TestCase):
    def setUp(self):
        self.c = Client()
        self.owner = None
        #self.owner =  User.objects.get(pk=1)
        
    def create_job(self):
        #TODO: check for 'ok' or resp value??
        
        #must make POST request
        response = self.c.get('/homepage/api/job/n/')
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'] , "must make POST request")
        
        # missing required fields
        response = self.c.post('/homepage/api/job/n/', {'name' : 'job1', \
                                                         'description' : 'test job', \
                                                         'location' : 'somewhere'})
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "missing required fields")
        
        #DB creation error
        response = self.c.post('/homepage/api/job/n/', {'name' : 'job1', \
                                                         'location' : 'somewhere', \
                                                         'description' : 'test job', \
                                                         'price' : 5, \
                                                         'owner' : None}) # invalid price type 
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "DB creation error")
        
        #successful creation
        response = self.c.post('/homepage/api/user/n/', {'name' : 'job1', \
                                                         'location' : 'somewhere', \
                                                         'description' : 'test job', \
                                                         'price' : 5.0, \
                                                         'owner' : self.owner})
        #self.assertEqual(json.loads(response.content.decode('utf8'))['ok'], True) 

    def get_job(self, job_id):
        #must make GET request
        response = self.c.post('/homepage/api/job/'+str(job_id)+'/', {})
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "must make GET request")
        
        #job not found
        response = self.c.get('/homepage/api/job/10000/')
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "job not found")
        
        #success provided db has the job
        response = self.c.get('/homepage/api/job/'+str(job_id)+'/')
        #self.assertEqual(json.loads(response.content.decode('utf8'))['ok'], True)
        
    def update_job(self, job_id):
        #must make POST request
        response = self.c.get('homepage/api/job/u/')
        self.assertEqual(response['resp'], "must make POST request")
        
        #job not found
        response = self.c.post('homepage/api/job/u/', {'job_id' : job_id})
        self.assertEqual(response['resp'], "job not found")
        
        #no fields updated
        response = self.c.post('hompage/api/job/u/', {'job_id' : job_id})
        self.assertEqual(response['resp'], 'no fields updated')
        
        #success
        response = self.c.post('homepage/api/user/u/', {'job_id' : job_id, 'description' : 'New Description'})
        self.assertEqual(response['ok'], True)
        
    def get_all_jobs(self):
        #must make GET request
        response = self.c.post('/homepage/api/job/all/', {})
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "must make GET request")
        
        #What condition would this fail under? No db?
        
        #success
        response = self.c.get('/homepage/api/job/all/')
        self.assertEqual(json.loads(response.content.decode('utf8'))['ok'], True)
    def delete_job(self, job_id):
        #must make POST request
        response = self.c.get('/homepage/api/job/d/')
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "must make POST request")
        
        #invalid request parameters
        response = self.c.post('/homepage/api/job/d/', {'job_id' : 10000})
        self.assertEqual(json.loads(response.content.decode('utf8'))['resp'], "invalid request parameters")

        #success
        response = self.c.post('/homepage/api/job/d/', {'job_id' : job_id})
        self.assertEqual(response['ok'], True)
        
    def runTest(self):
        self.create_job()
        self.get_job(1)
        self.update_job(1)
        self.get_all_jobs()
        self.delete_job(1)
    def tearDown(self):
        pass




