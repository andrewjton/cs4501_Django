from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout
#from .forms import JobForm
import requests
import json

def index(request):
    response = requests.get('http://exp-api:8000/api/v1/job/all/')
    jsonJobsList = json.loads(response.content.decode("utf8"))['resp']
    #return HttpResponse(jsonJobsList)

    return render(request, 'home/index.html', {'allJobs': jsonJobsList})

def about(request):
    return render(request, 'home/about.html', {})

#front end  for recieving user input
def register(request):
    auth = request.COOKIES.get('auth')
    if auth:
       return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    return render(request, 'home/register.html', {})

def login(request):
    return render(request, 'home/login.html', {})

def addjob(request):
	#form = JobForm()
	#return render(request, 'home/addjob.html', {'form': form})
	return render(request, 'home/addjob.html', {})

def logout_view(request):
    logout(request)

def job(request, jobID):
    response = requests.get('http://exp-api:8000/api/v1/job/'+str(jobID)+"/")
    jsonJobsList = json.loads(response.content.decode("utf8"))['resp']    
    return render(request, 'home/job.html', {'job': jsonJobsList})
    
    
