import django_filters
from .models import APIRequest
from robocrm.models import RoboUser
from channels.models import Channel
from rest_framework import generics
from django.contrib.contenttypes.models import ContentType
from projects.models import Project


class APIRequestFilter(django_filters.FilterSet):

  def _updater_is_project(qs, value):
    if value:
      return qs.filter(updater_type_id = ContentType.objects.get_for_model(Project).id)
    else:
      return qs.exclude(updater_type_id = ContentType.objects.get_for_model(Project).id)

  updater_is_project = django_filters.BooleanFilter(action=_updater_is_project)

  class Meta:
    model = APIRequest
    fields = ('id', 'endpoint', 'extra', 'user', 'updater_is_project', 'updater_id', 'created_datetime', 'updated_datetime', 'success', 'meta', )


# TODO: clean this class up
class RoboUserFilter(django_filters.FilterSet):

  # Eliminates the need for user__ prefix in filter
  username = django_filters.CharFilter(name='user__username')
  first_name = django_filters.CharFilter(name='user__first_name')
  last_name = django_filters.CharFilter(name='user__last_name')
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
    fields = ('id', 'balance', 'machines', 'color', )


# TODO: now that active field is gone
# is seperate class still required?
class ChannelFilter(django_filters.FilterSet):

  created = django_filters.DateTimeFilter()
  updated = django_filters.DateTimeFilter()
    
  class Meta:
    model = Channel
    fields = ('id', 'name', 'created', 'updated')
