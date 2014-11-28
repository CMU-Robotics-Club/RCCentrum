from django.db import models
from django.utils import timezone
from django.conf import settings
from crm.models import UpdatedByModel

class Channel(UpdatedByModel):

  name = models.CharField(max_length=30, unique=True)

  value = models.TextField(null=True, blank=True)

  @property
  def active(self):
    time_threshold = timezone.now() - settings.CHANNEL_ACTIVE_TIME_DELTA
    return (self.updated_datetime > time_threshold)

  class Meta:
    ordering = ['id', ]

  def __str__(self):
    return self.name
