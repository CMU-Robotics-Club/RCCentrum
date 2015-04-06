from django.db import models
from crm.models import UpdatedByModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.models import Channel
from api.models import APIRequest
from robocrm.models import Machine
import logging
import json

import requests

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Channel)
def channel_save_handler(sender, **kwargs):
  """
  Send value of channel to Websocket Server whenever
  Channel saved.
  """

  from api.serializers import ChannelSerializer

  instance = kwargs.pop('instance')
  serialized = ChannelSerializer(instance)
  body = serialized.data

  url = 'http://localhost:1984/channels/'

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


@receiver(post_save, sender=APIRequest)
def api_request_save_handler(sender, **kwargs):
  """
  Send value of channel to Websocket Server whenever
  APIRequest saved.
  """

  from api.serializers import APIRequestSerializer

  instance = kwargs.pop('instance')
  serialized = APIRequestSerializer(instance)
  body = serialized.data

  url = 'http://localhost:1984/api_requests/'

  headers = {
    'Content-Type': 'application/json',
  }

  try:
    response = requests.post(url, headers=headers, data=json.dumps(body))
    logger.info("POSTed APIRequest to Websocket Server")
  except Exception as e:
    # If cannot send notification to WebSocket server,
    # it is likely not running
    # Gracefully fail, log failure, and continue save
    logger.info("Could not POST to Websocket Server")
    logger.debug(e)


@receiver(post_save, sender=Machine)
def machine_save_handler(sender, **kwargs):
  """
  Send value of channel to Websocket Server whenever
  Machine saved.
  """

  from api.serializers import MachineSerializer

  instance = kwargs.pop('instance')
  serialized = MachineSerializer(instance)
  body = serialized.data

  url = 'http://localhost:1984/machines/'

  headers = {
    'Content-Type': 'application/json',
  }

  try:
    response = requests.post(url, headers=headers, data=json.dumps(body))
    logger.info("POSTed APIRequest to Websocket Server")
  except Exception as e:
    # If cannot send notification to WebSocket server,
    # it is likely not running
    # Gracefully fail, log failure, and continue save
    logger.info("Could not POST to Websocket Server")
    logger.debug(e)
