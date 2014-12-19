from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^(?P<project_id>\d+)/$', views.detail_id, name='detail-id'),
  url(r'^(?P<project_name>[-\w]+)/$', views.detail_name, name='detail-name'),
  url(r'^(?P<project_id>\d+)/label$', views.label_id, name='label-id'),
  url(r'^(?P<project_name>[-\w]+)/label$', views.label_name, name='label-name'),
)