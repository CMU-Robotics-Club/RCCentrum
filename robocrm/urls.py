from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
  url(r'^crm/roboauth/(?P<rfid_tag>[0-9A-Fa-f]+)/(?P<mach_num>\d+)/', views.roboauth),
  url(r'^crm/add_card_event/', views.add_card_event),
  url(r'^crm/directory_info/(?P<andrewid>\w+)/', views.directory_info),
)
