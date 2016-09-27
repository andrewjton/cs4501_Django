from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.http import JsonResponse
from django.core import serializers #for json files
import datetime
import json

from .models import Job, User

# Create your views here.
def index(request):
    return HttpResponse("Hello Andrewsdf. Congrats, you're making progress! :)")

def getUser(request, user_id):
    if request.method == 'GET':
        data = serializers.serialize("json", [User.objects.get(pk=user_id)]) #creates a json object in data
        return HttpResponse(data)


def createUser(request):
    #Assumes required parameters passed in are valid!
    if request.method == 'POST':
        user = User.objects.create(username = request.POST.get("username",""), first_name = request.POST.get("first_name", ""), 
                                   last_name = request.POST.get("last_name", ""), dob = request.POST.get("dob", ""),
                                   date_created = datetime.datetime.now())
        user.save()
        return HttpResponse(request.POST.get("username"))
    
def getAllUsers(request):
    data =  serializers.serialize("json", User.objects.all())
    return HttpResponse(data)

def getJob(request, job_id):
    if request.method == 'GET':
        data = serializers.serialize("json", [Job.objects.get(pk=job_id)])
        return HttpResponse(data)

def createJob(request):
    #Assumes required parameters passed in are valid!
    if request.method == 'POST':
        job = Job.objects.create(name = request.POST.get("name",""), description = request.POST.get("description",""),
                                 price = request.POST.get("price",""), location = request.POST.get("location",""),
                                 taken = False)
        owner = request.POST.get("owner", "")
        if owner != "":
            try:
                user = User.objects.get(username = owner)
                job.owner = user
            except User.DoesNotExist:
                pass
        
        job.save()
        return(HttpResponse("job created"))

def getAllJobs(request):
    data = serializers.serialize("json", Job.objects.all())
    return HttpResponse(data)

