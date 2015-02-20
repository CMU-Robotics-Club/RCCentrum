from django.db import models
from crm.models import UpdatedByModel
from django.db.models.signals import pre_save
from django.dispatch import receiver
import logging
import json

import requests


logger = logging.getLogger(__name__)


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


@receiver(pre_save, sender=Channel)
def channel_save_handler(sender, **kwargs):
  """
  Send value of channel to Websocket Server whenever
  Channel saved again.
  """

  instance = kwargs.pop('instance')

  id = instance.id
  value = instance.value

  url = 'http://localhost:1984/channels/{}/'.format(id)

  body = {
    'value': value,
  }

  headers = {
    'Content-Type': 'application/json',
  }

  try:
    response = requests.post(url, headers=headers, data=json.dumps(body))
  except Exception as e:
    # If cannot send notification to WebSocket server,
    # it is likely not running
    # Gracefully fail, log failure, and continue save
    logger.info("Could not POST to Websocket Server")
    logger.debug(e)
