from django.shortcuts import render
from django.http import HttpResponse
import requests
import json

def index(request):
    response = requests.get('http://exp-api:8000/api/v1/job/all/')
    jsonJobsList = json.loads(response.content.decode("utf8"))['resp']
    #return HttpResponse(jsonJobsList)

    return render(request, 'home/index.html', {'allJobs': jsonJobsList})

def about(request):
    return render(request, 'home/about.html', {})

def job(request, jobID):
    response = requests.get('http://exp-api:8000/api/v1/job/'+str(jobID)+"/")
    jsonJobsList = json.loads(response.content.decode("utf8"))['resp']    
    return render(request, 'home/job.html', {'job': jsonJobsList})
    
    
