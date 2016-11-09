from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
import json
import requests
from django.contrib.auth import hashers
from django.views.decorators.csrf import csrf_exempt
from kafka import KafkaProducer
from elasticsearch import Elasticsearch

#why do we have to recreate the json object?
def getAllJobs(request):
    jobs_list = requests.get('http://models-api:8000/api/v1/job/all/').json()['resp']
    return JsonResponse({'resp': jobs_list})     
    
def getJob(request, jobID):
    job = requests.get('http://models-api:8000/api/v1/job/' + str(jobID) + '/').json()['resp']
    return JsonResponse({'resp': job})

def login(request):
    username = request.POST.get('username', 'none')
    posted_pass = request.POST.get('password', 'none')

    #get user from username
    response = requests.get('http://models-api:8000/api/v1/user/'+username+'/').json()

    if response['ok'] == True:
        #check passwords
        user = response['resp']
        user_pass = user['password']

        if hashers.check_password(posted_pass, user_pass):
            #create auth
            auth_resp = requests.post('http://models-api:8000/api/v1/auth/n/', data={"user_id":user['user_id']}).json()
            return JsonResponse(auth_resp)
    return JsonResponse(response)
    #return JsonResponse({'ok':False,'resp':'invalid password'})

def logout(request):
    auth = request.POST.get('auth', 'default')
    response = requests.post('http://models-api:8000/api/v1/auth/d/',data={'auth':auth}).json()
    return JsonResponse(response)
    
def createJob(request):
#	return JsonResponse({'resp': 'hi'})
    price = request.POST.get('price', 'default')
    location = request.POST.get('location', 'default')
    name = request.POST.get('name', 'default')
    description = request.POST.get('description', 'default')
    auth = request.POST.get('auth', 'default')
    #get username from auth
    response = requests.get('http://models-api:8000/api/v1/auth/gufa/' + auth + '/').json()
    if not response['ok']:
        return JsonResponse(response, safe=False)
    owner = response['resp'] #username as string
    response = requests.post('http://models-api:8000/api/v1/job/n/', data={'price': price, 'location': location, 'name': name, 'description': description, 'owner':owner}).json()
 
    #add message to kafka queue
    if not response['ok']:
        return JsonResponse(response, safe=False) #if the object isn't created
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    some_new_listing = {'title': name, 'description': description, 'id':response['resp']['job_id']}
    producer.send('new-listings-topic', json.dumps(some_new_listing).encode('utf-8'))
    return JsonResponse(response,safe=False)

def register(request):
    username = request.POST.get('username', 'none')
    password = request.POST.get('password', 'none')
    first_name = request.POST.get('first_name', 'none')
    last_name = request.POST.get('last_name', 'none')
    dob = request.POST.get('dob', 'none')
    user = requests.post('http://models-api:8000/api/v1/user/n/', data = {'username':username,
                                                                         'password':password,
                                                                         'first_name':first_name,
                                                                         'last_name':last_name,
                                                                         'dob':dob}).json()
    return JsonResponse(user, safe=False)

def search(request):
    if 'search' not in request.POST:
        return JsonResponse({'ok':False, 'resp':'no query string'})
    search = request.POST.get('search')
	es = Elasticsearch(['es'])
	if(es.indices.exists('listing_index')):
		result = es.search(index='listing_index', body={'query': {'query_string': {'query': search}}, 'size': 10})
		jobs_data = result['hits']['hits']
		job_list = []
		for job in jobs_data:
			jobs = {}
			jobs['title'] = job['_source']['title']
			jobs['id'] = job['_source']['id']
			jobs['description'] = job['_source']['description']
			job_list.append(jobs)
		return JsonResponse({'ok':True, 'resp':job_list}, safe=False)
	return JsonResponse({'ok':False, 'resp':'no index created'})