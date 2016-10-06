import requests
import datetime

def createUser():
	req = requests.post("http://localhost:8001/homepage/api/user/n/",data={'username':'a new user','dob':str(datetime.datetime.now())})
	print(req.text[:300] + '...')

def createJob():
	req = requests.post("http://localhost:8001/homepage/api/job/n/",data={"name":"new job", "description":"3 bedroom apt", "price":50, "location":"arlington", "owner":"user2"})
	print(req.text[:300] + '...')
	
createJob()


