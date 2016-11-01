from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/n/$', views.createUser, name='createUser'),
    url(r'^user/u/$', views.updateUser, name='updateUser'),
    url(r'^user/d/$', views.deleteUser, name='deleteUser'),
    url(r'^user/all/$', views.getAllUsers, name='getAllUsers'),
    url(r'^user/(?P<username>[\w.@+-]+)/$', views.getUser, name='getUser'),
    url(r'^job/n/$', views.createJob, name='createJob'),
    url(r'^job/u/$', views.updateJob, name='updateJob'),
    url(r'^job/all/$', views.getAllJobs, name='getAllJobs'),
    url(r'^job/d/$', views.deleteJob, name='deleteJob'),
    url(r'^job/available/$', views.availableJobs, name='availableJobs'),
    url(r'^job/(?P<job_id>[0-9]+)/$', views.getJob, name='getJob'),
    url(r'^auth/n/$', views.createAuth, name='createAuth'),
    url(r'^auth/d/$', views.deleteAuth, name='deleteAuth'),
    url(r'^auth/gufa/(?P<token>[\w.@+-]+)/$', views.getUserFromAuth, name='getUserFromAuth'),
    url(r'^auth/(?P<token>[\w.@+-]+)/$', views.getAuth, name='getAuth'),


]

