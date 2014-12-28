import django_filters
from .models import APIRequest
from robocrm.models import RoboUser
from channels.models import Channel
from rest_framework import generics

class APIRequestFilter(django_filters.FilterSet):

  project = django_filters.NumberFilter(name='updater_id')
    
  class Meta:
    model = APIRequest
    fields = ('id', 'endpoint', 'user', 'project', 'created_datetime', 'updated_datetime', 'success', 'meta', )


# TODO: clean this class up
class RoboUserFilter(django_filters.FilterSet):

  # Eliminates the need for user__ prefix in filter
  username = django_filters.CharFilter(name='user__username')
  first_name = django_filters.CharFilter(name='user__first_name')
  last_name = django_filters.CharFilter(name='user__last_name')
  is_active = django_filters.BooleanFilter(name='user__is_active')
  date_joined = django_filters.DateTimeFilter(name='user__date_joined')
  last_login = django_filters.DateTimeFilter(name='user__last_login')

  # TODO: make static method
  def magnetic_filter(qs, value):
    if value:
      return qs.filter(magnetic__gt=0)
    else:
      return qs.exclude(magnetic__gt=0)

  # TODO: make static method
  def rfid_filter(qs, value):
    if value:
      return qs.filter(rfid__gt=0)
    else:
      return qs.exclude(rfid__gt=0)

  magnetic = django_filters.BooleanFilter(action=magnetic_filter)
  rfid = django_filters.BooleanFilter(action=rfid_filter)
    
  class Meta:
    model = RoboUser
    fields = ('id', 'machines', )


# TODO: now that active field is gone
# is seperate class still required?
class ChannelFilter(django_filters.FilterSet):

  created = django_filters.DateTimeFilter()
  updated = django_filters.DateTimeFilter()
    
  class Meta:
    model = Channel
    fields = ('id', 'name', 'created', 'updated')
