from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils import timezone
from django.core import serializers
import json
import requests

def getAllJobs(request):
    all_jobs = requests.get('http://models-api:8000/api/v1/job/all/')
    jobs_list = all_jobs
    jobs_list = jobs_list.json()['resp']
    return JsonResponse({'resp': jobs_list})     
    
def getJob(request, jobID):
    response = requests.get('http://models-api:8000/api/v1/job/' + str(jobID) + '/')
    job = response.json()['resp']
    return JsonResponse({'resp': job})

#experience layer API call to create user
def createUser(request):
    try:
        username = request.POST.get('username', 'default')
        password = request.POST.get('password', 'default')
        first_name = request.POST.get('first_name', 'default')
        last_name = request.POST.get('last_name', 'default')
        dob = timezone.now();
        user = requests.post('http://models-api:8000/api/v1/user/n', data={"username": username, "password": password, "first_name": first_name, "last_name": last_name,"dob": dob})
    except:
        return _error_response(request, "Error in model layer")


def _error_response(request, error_msg):
    return JsonResponse({'ok': False, 'resp': error_msg})

def _success_response(request, resp=None):
    if resp:
        return JsonResponse({'ok': True, 'resp': resp})
    else:
        return JsonResponse({'ok': True})