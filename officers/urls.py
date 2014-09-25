from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^(?P<officer_id>\d+)/$', views.detail_id),
  url(r'^(?P<officer_username>\w+)/$', views.detail_name),
)