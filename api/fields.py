from rest_framework import serializers
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class ProjectActiveField(serializers.BooleanField):

  def to_native(self, obj):
    time_threshold = timezone.now() - timedelta(seconds=settings.PROJECT_ACTIVE_SECONDS)

    if obj is None:
      return False

    return (obj >= time_threshold)
