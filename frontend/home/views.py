from django.shortcuts import render
from django.http import HttpResponse
import requests
import json

def index(request):
    response = requests.get('http://exp-api:8000/api/v1/job/all/')
    jsonJobsList = json.loads(response.content.decode("utf8"))['resp']
    #return HttpResponse(jsonJobsList)

    return render(request, 'home/index.html', {'alljobs': jsonJobsList})

def about(request):
    return render(request, 'home/about.html', {})

def job(request, jobID):
    response = requests.get('http://exp-api:8000/api/v1/job/all/')
    
    jsonJobsList = json.loads(response.content.decode("utf8"))['resp']
    #get specific job that has given jobID
    return render(request, 'home/job.html', {'job': jsonJobsList})
    
    
