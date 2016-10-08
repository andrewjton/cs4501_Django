from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
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