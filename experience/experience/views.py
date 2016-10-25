from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
import json
import requests
from django.views.decorators.csrf import csrf_exempt


def getAllJobs(request):
    jobs_list = requests.get('http://models-api:8000/api/v1/job/all/').json()['resp']
    return JsonResponse({'resp': jobs_list})     
    
def getJob(request, jobID):
	job = requests.get('http://models-api:8000/api/v1/job/' + str(jobID) + '/').json()['resp']
	return JsonResponse({'resp': job})

def login(request):
    auth_token = requests.post('http://models-api:8000/api/v1/auth/n/', request.POST).json()['resp']
    return JsonResponse({'resp': job})

@csrf_exempt
def createJob(request):
#	return JsonResponse({'resp': 'hi'})
	price = request.POST.get('price', 'default')
	owner = request.POST.get('owner', 'default')
	location = request.POST.get('location', 'default')
	name = request.POST.get('name', 'default')
	taken = request.POST.get('taken', 'false')
	description = request.POST.get('description', 'default')
	response = requests.post('http://models-api:8000/api/v1/job/n/', data={'price': price, 'owner': owner, 'location': location, 'name': name, 'taken': 'false', 'description': description}).json()['resp']
	return JsonResponse({'resp': response})