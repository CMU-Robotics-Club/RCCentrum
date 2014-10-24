from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',

  # roboticsclub.org/crm
  # TODO: remove these 3 patterns when site switched over
  url(r'^roboauth/(?P<rfid_tag>[0-9A-Fa-f]+)/(?P<mach_num>\d+)/', views.roboauth),
  url(r'^roboauth/(?P<rfid_tag>[0-9A-Fa-f]+)/', views.roboauthall),
  url(r'^add_card_event/', views.add_card_event),

  # roboticsclub.org/
  url(r'^crm/roboauth/(?P<rfid_tag>[0-9A-Fa-f]+)/(?P<mach_num>\d+)/', views.roboauth),
  url(r'^crm/roboauth/(?P<rfid_tag>[0-9A-Fa-f]+)/', views.roboauthall),
  url(r'^crm/add_card_event/', views.add_card_event),
)