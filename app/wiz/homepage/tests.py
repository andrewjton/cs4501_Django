from django.test import TestCase

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from homepage.models import User, Job
import datetime
import views


#TODO: need separate classes for each model?
class ModelsTest(TestCase):
    def setUp(self):
        pass
    def runTest(self):
         user = User(username='username',                         
                    first_name='first name',                            
                    last_name='last name',                             
                    dob= datetime.datetime.now(),  
                    date_created=datetime.datetime.now()                        
                    )
         self.assertTrue(isinstance(user, User))
         job = Job(name='name',                         
                    description='description',                            
                    location='somewhere',                             
                    price= 5.0,  
                    date_created=datetime.datetime.now(),
                    take = False,
                    owner = user
                    ) 
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
        self.assertEqual(response['resp'] , "must make POST request")
        
        # missing required fields
        response = self.c.post('/homepage/api/user/n/', {'username' : 'user1', \
                                                         'first_name' : 'first_name', \
                                                         'dob' : datetime.datetime.now()})
        self.assertEqual(response['resp'], "missing requred fields")
        
        #DB creation error
        response = self.c.post('/homepage/api/user/n/', {'username' : 'user1', \
                                                         'first_name' : 'first_name', \
                                                         'last_name' : 'last_name', \
                                                         'dob' : "some time"}) #invalid datetime
        self.assertEqual(response['resp'], "DB creation error")
        
        #successful creation
        response = self.c.post('/homepage/api/user/n/', {'username' : 'user1', \
                                                         'first_name' : 'first_name', \
                                                         'last_name' : 'last_name', \
                                                         'dob' : datetime.datetime.now()})
        self.assertContains(response['ok'], True) 

    def get_user(self):
        #must make GET request
        response = self.c.post('homepage/api/user/1/', {})
        self.assertEqual(response['resp'], "must make GET request")
        
        #user not found
        response = self.c.get('homepage/api/user/10000')
        self.assertEqual(response['resp'], "user not found")
        
        #success provided db has a user
        response = self.c.get('homepage/api/user/1')
        self.assertEqual(resonse['ok'], True)
       
    def get_all_users(self):
        #must make GET request
        response = self.c.post('homepage/api/user/all', {})
        self.assertEqual(response['resp'], "must make GET request")
        
        #What condition would this fail under? No db?
        
        #success
        response = self.c.get('homepage/api/user/all')
        self.assertEqual(response['ok'], True)
        
    def update_user(self, user_id):
        #must make POST request
        response = self.c.get('homepage/api/user/update/'+user_id+"/")
        self.assertEqual(response['resp'], "must make POST request")
        
        #user not found
        response = self.c.post('homepage/api/user/update/nonexistent_user/')
        self.assertEqual(response['resp'], "user not found")
        
        #no fields updated
        response = self.c.post('hompage/api/user/update/'+user_id+'/', {})
        self.assertEqual(response['resp'], 'no fields updated')
        
        #success
        response = self.c.post('homepage/api/user/update/'+user_id+'/', {'first_name' : 'New First Name'})
        self.assertEqual(response['ok'], 'True')
        
    def runTest(self):
        self.create_user()
        self.get_user()
        self.get_all_users()
        self.update_user(1) #1 is dummy user
        
    def tearDown(self):
        pass




class TestJobAPI(TestCase):
    def setUp(self):
        self.c = Client()
        
    def create_job(self):
        #TODO: check for 'ok' or resp value??
        
        #must make POST request
        response = self.c.get('/homepage/api/job/n/')
        self.assertEqual(response['resp'] , "must make POST request")
        
        # missing required fields
        response = self.c.post('/homepage/api/job/n/', {'name' : 'job1', \
                                                         'description' : 'test job', \
                                                         'location' : 'somewhere'})
        self.assertEqual(response['resp'], "missing requred fields")
        
        #DB creation error
        response = self.c.post('/homepage/api/job/n/', {'name' : 'job1', \
                                                         'location' : 'somewhere', \
                                                         'description' : 'test job', \
                                                         'price' : '$5',}) # invalid price type 
        self.assertEqual(response['resp'], "DB creation error")
        
        #successful creation
        response = self.c.post('/homepage/api/user/n/', {'name' : 'job1', \
                                                         'location' : 'somewhere', \
                                                         'description' : 'test job', \
                                                         'price' : 5.0})
        self.assertContains(response['ok'], True) 

    def get_job(self):
        #must make GET request
        response = self.c.post('homepage/api/job/1/', {})
        self.assertEqual(response['resp'], "must make GET request")
        
        #job not found
        response = self.c.get('homepage/api/job/10000')
        self.assertEqual(response['resp'], "job not found")
        
        #success provided db has a user
        response = self.c.get('homepage/api/job/1')
        self.assertEqual(resonse['ok'], True)
        
    def update_job(self, job_id):
        #must make POST request
        response = self.c.get('homepage/api/job/update/'+job_id+"/")
        self.assertEqual(response['resp'], "must make POST request")
        
        #job not found
        response = self.c.post('homepage/api/job/update/nonexistent_job/')
        self.assertEqual(response['resp'], "job not found")
        
        #no fields updated
        response = self.c.post('hompage/api/job/update/'+job_id+'/', {})
        self.assertEqual(response['resp'], 'no fields updated')
        
        #success
        response = self.c.post('homepage/api/user/update/'+job_id+'/', {'description' : 'New Description'})
        self.assertEqual(response['ok'], 'True')
        
    def get_all_jobs(self):
        #must make GET request
        response = self.c.post('homepage/api/job/all', {})
        self.assertEqual(response['resp'], "must make GET request")
        
        #What condition would this fail under? No db?
        
        #success
        response = self.c.get('homepage/api/job/all')
        self.assertEqual(response['ok'], True)
    
    def runTest(self):
        self.create_job()
        self.get_job()
        self.update_job()
        self.get_all_jobs()
    def tearDown(self):
        pass




