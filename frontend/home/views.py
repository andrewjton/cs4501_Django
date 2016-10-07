from django.shortcuts import render
from django.http import HttpResponse
import requests
import json

def index(request):
    return render(request, 'home/index.html', {})

def about(request):
    return render(request, 'home/about.html', {})

def clean(request):
    response = requests.get('http://exp-api:8000/api/job/all')
    jsonJobsList = json.loads(response.content.decode())['resp']
    return render(request, 'home/clean.html', {'allJobs': jsonJobsList})
