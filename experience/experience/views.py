from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
import json
import requests
from django.contrib.auth import hashers
from django.views.decorators.csrf import csrf_exempt

#why do we have to recreate the json object?
def getAllJobs(request):
    jobs_list = requests.get('http://models-api:8000/api/v1/job/all/').json()['resp']
    return JsonResponse({'resp': jobs_list})     
    
def getJob(request, jobID):
    job = requests.get('http://models-api:8000/api/v1/job/' + str(jobID) + '/').json()['resp']
    return JsonResponse({'resp': job})

@csrf_exempt #need to remove later??
def login(request):
    username = request.POST.get('username', 'no_user')
    posted_pass = request.POST.get('password', 'no_password')
    user = requests.get('http://models-api:8000/api/v1/user/'+username+'/').json()
    if user['ok'] == True:
        #check passwords
        user_pass = user['resp']['password']
        if hashers.check_password(posted_pass, user_pass):
            #create auth
            auth_token = requests.post('http://models-api:8000/api/v1/auth/n/', data={"user_id":user.id}).json()['resp']
            return JsonResponse({'resp':auth_token})
    return JsonResponse({'resp': user_pass})

    
def _error_response(request, error_msg):
    return JsonResponse({'ok': False, 'resp': error_msg})

def _success_response(request, resp=None):
    if resp:
        return JsonResponse({'ok': True, 'resp': resp})
    else:
        return JsonResponse({'ok': True})