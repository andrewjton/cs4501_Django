from django.shortcuts import render
from django import forms
from django.http import HttpResponse
import requests
import json
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import *
from django.contrib.auth import hashers
from django.contrib import messages
from django.shortcuts import render_to_response
def index(request):
    response = requests.get('http://exp-api:8000/api/v1/job/all/').json()['resp']

    return render(request, 'home/index.html', {'allJobs': response})

def about(request):
    return render(request, 'home/about.html', {})

def login(request):
    auth = request.COOKIES.get('auth')
    if auth:
        return HttpResponse("redirect")
    if request.method == 'GET':
        login_form = LoginForm()
        next = request.GET.get('login') or reverse('index')
        return render(request, 'home/login.html', {'form': login_form})#why need this?
    f = LoginForm(request.POST)
    if not f.is_valid():
        return HttpResponse("didnt fill in forms properly")
    username = f.cleaned_data['username']
    password = f.cleaned_data['password']
    next = reverse('index')
    response = requests.post('http://exp-api:8000/api/v1/login/', data={'username':username, 'passowrd':password}).json()
    if not response['ok']:
        #error occurred
        return HttpResponse(response['resp'])
    auth_token = response['resp']
    response =HttpResponseRedirect('home/index.html')
    response.set_cookie("auth", auth_token)
    return response


def register(request):
    return render(request, 'home/register.html', {})

def job(request, jobID):
    response = requests.get('http://exp-api:8000/api/v1/job/'+str(jobID)+"/")
    jsonJobsList = json.loads(response.content.decode("utf8"))['resp']    
    return render(request, 'home/job.html', {'job': jsonJobsList})
    
    
