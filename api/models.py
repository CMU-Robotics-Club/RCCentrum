from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from crm.models import UpdatedByModel
from projects.models import Project
from robocrm.models import RoboUser

class APIRequest(UpdatedByModel):
  """
  Log of API Requests for /rfid, /magnetic,
  /users/:id/email, and /users/:id/rfid
  """

  """
  Name of the request endpoint.
  """
  endpoint = models.CharField(max_length=30)
  
  """
  Which RoboUser this request is for.
  (Can be none if invalid request)
  """
  user = models.ForeignKey(RoboUser, null=True)
  
  """
  Extra endpoint and request specific information.
  """
  meta = models.TextField(null=True)

  def __str__(self):
    return self.endpoint
