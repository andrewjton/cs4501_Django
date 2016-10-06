from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'home/index.html', {})

def about(request):
    return render(request, 'home/about.html', {})

def clean(request):
	job = requests.get('http://experience:8000/api/job/all')
	deserial = json.loads(job.text)
    return render(request, 'home/clean.html', {'allJobs': deserial})
