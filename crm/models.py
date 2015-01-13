from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class TimeStampedModel(models.Model):
  """
  A model that has a created and modified datetime.
  """

  # TODO: look into auto_now_add and auto_now more
  # as some posts claim it causes issues in certain
  # circumstances
  # auto_now_add and auto_now implicity set editable to False
  created_datetime = models.DateTimeField(auto_now_add=True)
  updated_datetime = models.DateTimeField(auto_now=True)

  class Meta:
    abstract = True


class UpdatedByModel(TimeStampedModel):
  """
  A model that stores the last RoboUser or Project that
  updated it.
  """

  """
  Project or User that made update.
  Should not be editable since it is automatically set
  (not through admin interface which the editable field is for).
  """
  updater_type = models.ForeignKey(ContentType, editable=False)
  updater_id = models.PositiveIntegerField(editable=False)
  updater_object = GenericForeignKey('updater_type', 'updater_id')

  class Meta:
    abstract = True
