from django.conf.urls import url

from home import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
	url(r'^register/$', views.register, name='register'),
    url(r'^job/(?P<jobID>\d+)$', views.job, name="job"),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^addjob/$', views.addjob, name='addjob'),
]
