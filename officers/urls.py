from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
  url(r'^$', views.index),
  url(r'^(?P<officer_id>\d+)/$', views.detail),
)