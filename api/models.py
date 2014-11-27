from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from crm.models import TimeStampedModel
from projects.models import Project
from robocrm.models import RoboUser

class APIRequest(TimeStampedModel):
  
  """
  Name of the request endpoint.
  """
  endpoint = models.CharField(max_length=30)

  """
  Project or User that made request.
  """
  requester_type = models.ForeignKey(ContentType)
  requester_id = models.PositiveIntegerField()
  requester_object = GenericForeignKey('requester_type', 'requester_id')
  
  """
  If this is a User lookup API call this fields
  contains who the lookup is for.
  """
  user = models.ForeignKey(RoboUser, null=True)
  
  """
  Extra endpoint specific information.
  """
  meta = models.CharField(max_length=50, null=True, blank=True)

  def __str__(self):
    return self.endpoint
