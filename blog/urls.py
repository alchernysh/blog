from django.conf.urls import *
from . import views

urlpatterns = [
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^email_confirmation/$', views.email_confirmation, name='email_confirmation'),
	url(r'^change_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
		views.change_password, name='change_password'),
	url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^notes_list/$', views.notes, name='notes'),
    url(r'^note_new/$', views.note_new, name='note_new'),
    url(r'^note_edit/id=(?P<id>[0-9]+)/$', views.note_edit, name='note_edit'),
    url(r'^note_detail/id=(?P<id>[0-9]+)/$', views.note_detail, name='note_detail'),
    url(r'^note_delete/id=(?P<id>[0-9]+)/$', views.note_delete, name='note_delete'),
    url(r'^$', views.index, name = 'index' ),
]
