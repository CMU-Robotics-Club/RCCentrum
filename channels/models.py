from django.db import models
from django.utils import timezone
from django.conf import settings

class Channel(models.Model):

  name = models.CharField(max_length=30, unique=True)

  created = models.DateTimeField(default=timezone.now)
  updated = models.DateTimeField(default=timezone.now)

  value = models.TextField(null=True, blank=True)

  def save(self, *args, **kwargs):
    self.updated = timezone.now()
    return super().save(*args, **kwargs)

  @property
  def active(self):
    time_threshold = timezone.now() - settings.CHANNEL_ACTIVE_TIME_DELTA
    return (self.updated > time_threshold)

  def __str__(self):
    return self.name
