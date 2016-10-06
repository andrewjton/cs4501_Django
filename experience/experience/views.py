from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
import json
import requests

def getAllJobs(request):
    
    all_jobs = requests.get('http://entity:8000/api/job/all')
    deserial_jobs = json.loads(all_jobs.text)
    for job in deserial_job:
            curr_id = int(job['pk'])
            info[curr_id] = str(job['fields']['name'])
    return JsonResponse(info, content_type='application/json')