"""wiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import home

from django.conf.urls.static import static #for static hello world
from django.conf import settings #for static hello world

urlpatterns = [
    url(r'^$', home.index, name='index'), #for static hello world
    url(r'^admin/', include(admin.site.urls)),
    url(r'^homepage/', include('homepage.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) #for static hello world
