from django.shortcuts import render
from django.http import HttpResponse
import requests
import json

def index(request):
    return render(request, 'home/index.html', {})
    response = requests.get('http://exp-api:8000/api/job/all')
    jsonJobsList = json.loads(response.content.decode("utf8"))['resp']
    return render(request, 'home/index.html', {'allJobs': jsonJobsList})

def about(request):
    return render(request, 'home/about.html', {})

def job(request, jobID):
    return render(request, 'home/job.html', {})
    response = requests.get('http://exp-api:8000/api/job/all')
    jsonJobsList = json.loads(response.content.decode("utf8"))['resp']
    #get specific job that has given jobID
    return render(request, 'home/job.html', {'job': jsonJobsList})
    
    
