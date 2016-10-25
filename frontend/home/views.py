from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.contrib.auth import logout
#from .forms import JobForm
import requests
import json
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import *
from django.contrib.auth import hashers
from django.contrib import messages
from django.shortcuts import render_to_response
from django.utils import timezone

def index(request):
    response = requests.get('http://exp-api:8000/api/v1/job/all/').json()['resp']

    return render(request, 'home/index.html', {'allJobs': response})

def about(request):
    return render(request, 'home/about.html', {})

#front end  for recieving user input

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
        return HttpResponse("didnt fill in forms properly") #put this in template as error message
    username = f.cleaned_data['username']
    password = f.cleaned_data['password']
    first_name  = f.cleaned_data['first_name']
    last_name = f.cleaned_data['last_name']
    dob = timezone.now();
    next = reverse('index')
    response = requests.post('http://exp-api:8000/api/v1/login/', data={"username": username, "password": password, "first_name": first_name, "last_name": last_name,"dob": dob}).json()
    if not response['ok']:
        #error occurred
        return HttpResponse(response['resp'])
    auth_token = response['resp']
    response =HttpResponseRedirect('home/index.html')
    response.set_cookie("auth", auth_token)
    return response


def login(request):
    return render(request, 'home/login.html', {})

def addjob(request):
	if request.method == 'GET':
		form = JobForm()
		return render(request, 'home/addjob.html', {'form': form})
	
	f = JobForm(request.POST)
	if not f.is_valid():
		return HttpResponse("didnt fill in forms properly"); #put this in template as error message
	name = f.cleaned_data['name']
	description = f.cleaned_data['description']
	price = f.cleaned_data['price']
	location = f.cleaned_data['location']
	owner = 1
	'cleaner' not in request.POST or \
	response = requests.post('http://exp-api:8000/api/v1/createJob/', data={'price': price, 
																			'owner': owner, 
																			'location': location, 
																			'name': name, 
																			'taken': 'false', 
																			'description': description}).json()
#	if not response['ok']:
#        #error occurred
#		return HttpResponse(response['resp'])
	response =HttpResponseRedirect('/')
	return response
	
def logout_view(request):
    logout(request)

def job(request, jobID):
    response = requests.get('http://exp-api:8000/api/v1/job/'+str(jobID)+"/")
    jsonJobsList = json.loads(response.content.decode("utf8"))['resp']    
    return render(request, 'home/job.html', {'job': jsonJobsList})
    
    
