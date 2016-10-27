from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
import json
import requests
from django.contrib.auth import hashers
from django.views.decorators.csrf import csrf_exempt

#why do we have to recreate the json object?
def getAllJobs(request):
    jobs_list = requests.get('http://models-api:8000/api/v1/job/all/').json()['resp']
    return JsonResponse({'resp': jobs_list})     
    
def getJob(request, jobID):
    job = requests.get('http://models-api:8000/api/v1/job/' + str(jobID) + '/').json()['resp']
    return JsonResponse({'resp': job})

@csrf_exempt #need to remove later??
def login(request):
    username = request.POST.get('username', 'none')
    posted_pass = request.POST.get('password', 'none')

    response = requests.get('http://models-api:8000/api/v1/user/'+username+'/').json()

    if response['ok'] == True:
        #check passwords
        user = response['resp']
        user_pass = user['password']

        if hashers.check_password(posted_pass, user_pass):
            #create auth
            auth_resp = requests.post('http://models-api:8000/api/v1/auth/n/', data={"user_id":user['user_id']}).json()
            return JsonResponse(auth_resp)
        else:
            #return invalid password
            pass
    return JsonResponse(user)

@csrf_exempt
def createJob(request):
#	return JsonResponse({'resp': 'hi'})
	price = request.POST.get('price', 'default')
	owner = request.POST.get('owner', 'default')
	cleaner = request.POST.get('cleaner', 'default')
	location = request.POST.get('location', 'default')
	name = request.POST.get('name', 'default')
	description = request.POST.get('description', 'default')
	response = requests.post('http://models-api:8000/api/v1/job/n/', data={'price': price, 'location': location, 'name': name, 'description': description, 'owner':owner, 'cleaner':cleaner}).json()['resp']
	return JsonResponse({'resp': response})

@csrf_exempt
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
    
def _error_response(request, error_msg):
    return JsonResponse({'ok': False, 'resp': error_msg})

def _success_response(request, resp=None):
    if resp:
        return JsonResponse({'ok': True, 'resp': resp})
    else:
        return JsonResponse({'ok': True})
