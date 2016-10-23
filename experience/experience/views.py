from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
import json
import requests


def getAllJobs(request):
    jobs_list = requests.get('http://models-api:8000/api/v1/job/all/').json()['resp']
    return JsonResponse({'resp': jobs_list})     
    
def getJob(request, jobID):
    job = requests.get('http://models-api:8000/api/v1/job/' + str(jobID) + '/').json()['resp']
    return JsonResponse({'resp': job})

def login(request):
    auth_token = requests.post('http://models-api:8000/api/v1/auth/n/', request.POST).json()['resp']
    return JsonResponse({'resp': auth_token})
    
