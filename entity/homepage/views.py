from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.http import JsonResponse
from django.core import serializers #for json files
from django.forms.models import model_to_dict
from django.contrib.auth import hashers
from django.utils import timezone
import json

from .models import Job, User, Authenticator
from django import db

# Create your views here.

### API ###
# createUser()
# updateUser()
# getUser(username)
# getAllUsers()
# deleteUser()
# createJob()
# updateJob()
# getJob(job_id)
# getAllJobs(job_id)
# deleteJob()
# createAuth()
# getAuth()
# deleteAuth()

#error response
#success response

def index(request):
    return HttpResponse("You made it to the api!")

def createUser(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'username' not in request.POST or \
        'password' not in request.POST or \
        'first_name' not in request.POST or \
        'last_name' not in request.POST or \
        'dob' not in request.POST:
        return _error_response(request, "missing required fields")
    try:
        user = User.objects.create(username = request.POST["username"], \
                                   password = hashers.make_password(request.POST['password']), \
                                    first_name = request.POST["first_name"], \
                                    last_name = request.POST["last_name"], \
                                    dob = request.POST["dob"], \
                                    date_created = timezone.now())
        user.save()
    except:
        return _error_response(request, "DB creation error")
    return _success_response(request, {'userid': user.pk})

def updateUser(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    try:
        user = User.objects.get(pk=request.POST['user_id'])
    except:
        return _error_response(request, "user not found")
    changed = False
    if 'first_name' in request.POST:
        user.first_name = request.POST['first_name']
        changed = True
    if 'last_name' in request.POST:
        user.last_name = request.POST['last_name']
        changed = True
    if 'dob' in request.POST:
        user.dob = request.POST['dob']
        changed = True
    if not changed:
        return _error_response(request, "no fields updated")
    user.save()
    return _success_response(request)

def getUser(request, username):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")
    try:
        u = User.objects.filter(username=username)
    except:
        return _error_response(request, "user not found")
    return _success_response(request, {'username': u.username,      
                                       'first_name': u.first_name,          
                                       'last_name': u.last_name,          
                                       'dob': u.dob,    
                                       'date_created': u.date_created 
                                       })

def getAllUsers(request):
    if request.method!='GET':
        return _error_response(request, "must make GET request")
    data = User.objects.all()
    data = list(map(model_to_dict, data))
    return _success_response(request, data)

def deleteUser(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    try:
        User.objects.get(pk=int(request.POST['username'])).delete()
    except:
        return _error_response(request, "invalid request parameters")
    return _success_response(request)



def createJob(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'name' not in request.POST or \
        'description' not in request.POST or \
        'price' not in request.POST or \
        'location' not in request.POST or \
        'cleaner' not in request.POST or \
        'owner' not in request.POST:
        return _error_response(request, "missing required fields")
    try:
        j = Job(name=request.POST['name'],
            description=request.POST['description'],
            price=request.POST['price'],
            location=request.POST['location'],
            owner= User.objects.get(username = request.POST['owner']),
            cleaner=User.objects.get(username = request.POST['user']),
            date_created = timezone.now(),
            taken=False)

        j.save()
    except:
        return _error_response(request, "DB creation error")
    
    return _success_response(request, {'job_id': j.pk})

def updateJob(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    try:
        job = Job.objects.get(pk=request.POST['job_id'])
    except:
        return _error_response(request, "job not found")
    changed = False
    try:
        if 'description' in request.POST:
            job.description = request.POST['description']
            changed = True
        if 'price' in request.POST:
            job.price = request.POST['price']
            changed = True
        if 'location' in request.POST:
            job.location = request.POST['location']
            changed = True
        if 'taken' in request.POST:
            job.taken = request.POST['taken']
            changed = True
    except:
        _error_response(request, 'invalid field value')
    if not changed:
        return _error_response(request, "no fields updated")
    job.save()
    return _success_response(request)

def getJob(request, job_id):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")
    try:
        j = Job.objects.get(pk=job_id)
    except:
        return _error_response(request, "job not found")
    try:
        owner = User.objects.filter(username=j.owner).first().username
    except:
        return _error_response(request, "owner not found")
    return _success_response(request, {'name': j.name,      
                                       'description': j.description,          
                                       'owner': owner,         
                                       'price': j.price,    
                                       'location': j.location
                                       })

def getAllJobs(request):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")
    data = Job.objects.all()
    data = list(map(model_to_dict, data))
    return _success_response(request, data)

def deleteJob(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    try:
        Job.objects.get(pk=int(request.POST['job_id'])).delete()
    except:
        return _error_response(request, "invalid request parameters")
    return _success_response(request)


def availableJobs(request):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")

    try:
        ts = _available_jobs()
    except db.Error:
        return _error_response(request, "db error")

    return _success_response(request, {'recent_things': ts})

def _available_jobs():
    ts = Job.objects.filter(taken=False)
    ts = list(map(model_to_dict, ts))
    return ts

def createAuth(request):
    if request.method != 'POST':
        return _error_response(request, 'must make POST request')
    if 'username' not in request.POST or \
        'password' not in request.POST:
        return _error_response(request, 'missing required fields')
    if(Authenticator.objects.filter(username=request.POST['username']).exists()):
        return _error_response(request, 'user already authenticated')
    try:
        u = User.objects.get(pk=request.POST['username'], password=request.POST['password'])
    except:
        return _error_response("username password combination not found")
    try:
        code = hmac.new(key= settings.SECRET_KEY.encode('utf-8'), msg = os.urandom(32), digestmod = 'sha256').hexdigest()
        token = Authenticator.objects.create(authenticator=code, \
                                             username=request.POST['username'], \
                                             date_created=timezone.now())
    except:
        return _error_response(request, "creation error")
    return _success_response(request, token)

#should be post request for security?
def getAuth(request, token):
    if request.method != 'GET':
        return _error_response(request, 'must make GET request')
    try:
        auth = Authenticator.objects.get(pk=token)
    except:
        return _error_response("token not found")
    return _success_response(request)

def deleteAuth(request):
    if request.method != 'POST':
        return _error_response(request, 'must make POST request')
    if 'username' not in request.POST:
        return _error_response(request, 'missing required fields')
    try:
        Authenticator.objects.filter(username=request.POST['username']).delete()
    except:
        return _error_response(request, "deletion error")
    return _success_response(request)
        

def _error_response(request, error_msg):
    return JsonResponse({'ok': False, 'resp': error_msg})

def _success_response(request, resp=None):
    if resp:
        return JsonResponse({'ok': True, 'resp': resp})
    else:
        return JsonResponse({'ok': True})

