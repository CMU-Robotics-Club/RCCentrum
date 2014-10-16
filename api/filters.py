import django_filters
from robocrm.models import RoboUser
from .serializers import RoboUserSerializer
from rest_framework import generics

# TODO: clean this class up
class RoboUserFilter(django_filters.FilterSet):

  # Eliminates the need for user__ prefix in filter
  username = django_filters.CharFilter(name='user__username')
  email = django_filters.CharFilter(name='user__email')
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
