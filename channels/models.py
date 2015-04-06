from django.db import models
from crm.models import UpdatedByModel

class Channel(UpdatedByModel):
  """
  Used to pass messages amongst projects and users.
  Any project can create, read, and write to any channel
  through API.
  Any user can created, read, and write to any channel
  through Admin interface.
  """

  name = models.CharField(max_length=30, unique=True)

  value = models.TextField(null=True, blank=True)

  description = models.TextField(null=True, blank=True, help_text="Description about what this channel is used for")

  class Meta:
    ordering = ['id', ]

  def __str__(self):
    return self.name
