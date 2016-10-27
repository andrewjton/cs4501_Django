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
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'GET':
        login_form = LoginForm()
        next = request.GET.get('login') or reverse('index')
        return render(request, 'home/login.html', {'form':login_form})

    f = LoginForm(request.POST)
    if not f.is_valid():
        login_form = LoginForm()
        return render(request, 'home/login.html', {'errorMessage': "Please fill out all fields",'form': login_form})
    username = f.cleaned_data['username']
    password = f.cleaned_data['password']
    next = reverse('index')
    response = requests.post('http://exp-api:8000/api/v1/login/', data={'username':username, 'password':password}).json()
    if not response:
        #error occurred
        login_form = LoginForm()
        return render(request, 'home/login.html', {'errorMessage': "DB write error",'form': login_form})
    auth_token = response['resp']
    response =HttpResponseRedirect('index')
    response.set_cookie("auth", auth_token)
    return response

def logout(request):
	auth = request.COOKIES.get('auth')
	if not auth:
		return HttpResponseRedirect(reverse('login'))
	response = requests.post('http://exp-ap:8000/api/v1/logout/')


def addjob(request):
    auth = request.COOKIES.get('auth')
    if not auth:
        return HttpResponseRedirect(reverse("login"))

    if request.method == 'GET':
        form = JobForm()
        return render(request, 'home/addjob.html', {'form': form})
    f = JobForm(request.POST)
    if not f.is_valid():
        form = JobForm()
        return render(request, 'home/addjob.html', {'errorMessage': "Please fill out all fields",'form': form})
    name = f.cleaned_data['name']
    description = f.cleaned_data['description']
    price = f.cleaned_data['price']
    location = f.cleaned_data['location']
    owner = "user1"
    cleaner = "user1"
    response = requests.post('http://exp-api:8000/api/v1/job/n/', data={'price': price, \
                                                                            'owner': owner, \
                                                                           'cleaner': cleaner, \
                                                                           'location': location, \
                                                                           'name': name, \
                                                                           'auth':auth, \
                                                                           'description': description}).json()
    if not response['ok']:
        #error occurred
        return render(request, 'home/addjob.html', {'errorMessage': "DB Write error",'form': form})
    response = HttpResponseRedirect('/')
    return response

def logout_view(request):
    logout(request)

def register(request):
    if request.method =='GET':
        register_form = RegisterForm()
        return render(request, 'home/register.html', {'form': register_form})
    f = RegisterForm(request.POST)
    if not f.is_valid():
        register_form = RegisterForm()
        return render(request, 'home/register.html', {'errorMessage': "Please fill out all fields", 'form': register_form})
    username = f.cleaned_data['username']
    password = f.cleaned_data['password']
    first_name = f.cleaned_data['first_name']
    last_name = f.cleaned_data['last_name']
    dob = f.cleaned_data['date_of_birth']
    response = requests.post('http://exp-api:8000/api/v1/register/', data={'username':username,
                                                                           'password':password,
                                                                           'first_name':first_name,
                                                                           'last_name':last_name,
                                                                           'dob':dob}).json()
    next = reverse('login')
    if not response['ok']:
        return render(request, 'home/register.html', {'errorMessage': "Invalid signup", 'form': register_form})
    return HttpResponseRedirect(next)

    
def job(request, jobID):
    response = requests.get('http://exp-api:8000/api/v1/job/'+str(jobID)+"/")
    jsonJobsList = json.loads(response.content.decode("utf8"))['resp']    
    return render(request, 'home/job.html', {'job': jsonJobsList})
    
    
