from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'home/index.html', {})

def about(request):
    return render(request, 'home/about.html', {})

def clean(request):
    return render(request, 'home/clean.html', {})
