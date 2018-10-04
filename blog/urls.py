from django.conf.urls import *
from . import views

urlpatterns = [
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
    url(r'^$', views.index, name = 'index' ),
]
