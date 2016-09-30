from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.http import JsonResponse
from django.core import serializers #for json files
from django.forms.models import model_to_dict
import datetime
import json

from .models import Job, User
from django import db

# Create your views here.

### API ###
#1 createUser
#2 createJob
#3 getAllUsers
#4 getAllJobs
#5 getUser
#6 getJob
#updateUser
#updateJob
#deleteUser
#deleteJob
#take job

#error response
#success response

def index(request):
    return HttpResponse("You made it to the home page!")

#1 createUser
def createUser(request): 
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'first_name' not in request.POST or 'last_name' not in request.POST or'dob' not in request.POST or 'username' not in request.POST:
        return _error_response(request, "missing required fields")

    u = User(username=request.POST['username'],                         
                    first_name=request.POST['first_name'],                            
                    last_name=request.POST['last_name'],                             
                    dob=request.POST['dob'],  
                    date_created=datetime.datetime.now()                        
                    )

    try:
        u.save()
    except db.Error:
        return _error_response(request, "db error")

    return _success_response(request, {'user_id': u.pk})

#2 createJob
def createJob(request):
    if request.method != 'POST':
        return _error_response(request, "must make a POST request")
    if 'name' not in request.POST or 'description' not in request.POST or 'price' not in request.POST or 'location' not in request.POST or 'owner' not in request.POST:
        return _error_response(request, "missing required fields")
    
    j = Job(name=request.POST['name'],
            description=request.POST['description'],
            price=request.POST['price'],
            location=request.POST['location'],
            owner= User.objects.get(username = request.POST['owner']),
            taken=False)
    try:
        j.save()
    except db.Error:
        return _error_response(request, "db error")
    
    return _success_response(request, {'job_id': j.pk})

#3 getAllUsers
def getAllUsers(request):
    if request.method!='GET':
        return _error_response(request, "must make a GET request")

    data = User.objects.all()
    data = list(map(model_to_dict, data))

    return _success_response(request, data)

#4 getAllJobs
def getAllJobs(request):
    if request.method != 'GET':
        return _error_response(request, "must make a GET request")
    data = Job.objects.all()
    data = list(map(model_to_dict, data))
    return _success_response(request, data)

#getUser
def getUser(request, user_id):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")

    try:
        u = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return _error_response(request, "user not found")

    return _success_response(request, {'username': u.username,      
                                       'first_name': u.first_name,          
                                       'last_name': u.last_name,          
                                       'dob': u.dob,    
                                       'date_created': u.date_created 
                                       })

#getJob
def getJob(request, job_id):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")

    try:
        j = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        return _error_response(request, "user not found")

    return _success_response(request, {'name': j.name,      
                                       'description': j.description,          
                                       'owner': (User.objects.filter(username=j.owner)).first().username,          
                                       'price': j.price,    
                                       'location': j.location
                                       })




#error_response
def _error_response(request, error_msg):
    return JsonResponse({'ok': False, 'error': error_msg})

#success_response
def _success_response(request, resp=None):
    if resp:
        return JsonResponse({'ok': True, 'resp': resp})
    else:
        return JsonResponse({'ok': True})








#update job
#update user
#delete user
def deleteUser(request, user_id):
    User.objects.get(pk=user_id).delete()
    return HttpResponse(user_id);
#delete job
def deleteJob(request, user_id):
    Job.objects.get(pk=user_id).delete()
    return HttpResponse(user_id);