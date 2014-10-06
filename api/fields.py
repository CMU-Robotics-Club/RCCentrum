from rest_framework import serializers
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils import timezone
from datetime import timedelta

class APIImageField(serializers.ImageField):

  def to_native(self, obj):
    parent = super(APIImageField, self).to_native(obj)
    site = Site.objects.get_current()
    url = "{}{}{}".format(site.domain, settings.MEDIA_URL, parent)
    return url


class ProjectActiveField(serializers.BooleanField):

  def to_native(self, obj):
    time_threshold = timezone.now() - timedelta(seconds=settings.PROJECT_ACTIVE_SECONDS)
    print(self.__dict__)
    print(obj)

    if obj is None:
      return False

    return (obj >= time_threshold)
