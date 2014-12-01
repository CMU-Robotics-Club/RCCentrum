from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from crm.models import UpdatedByModel
from projects.models import Project
from robocrm.models import RoboUser

class APIRequest(UpdatedByModel):

  """
  Name of the request endpoint.
  """
  endpoint = models.CharField(max_length=30)
  
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
