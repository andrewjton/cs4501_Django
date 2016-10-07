from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
import json
import requests

def getAllJobs(request):
    #return HttpResponse("hi")
    all_jobs = requests.get('http://models-api:8000/homepage/api/job/all')
    jobs_list = json.loads(all_jobs.content.decode('utf8'))['resp']
    return JsonResponse({'resp': jobs_list})     

