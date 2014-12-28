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
  endpoint = models.CharField(max_length=30, editable=False)
  
  """
  Which RoboUser this request is for.
  (Can be none if invalid request)
  """
  user = models.ForeignKey(RoboUser, null=True, editable=False)
  
  """
  Project editable field.
  Should be set to False if a User lookup was successful
  but the User did not have permissions to perform the intended 
  action.
  (ex. User successfull yauthenticated for Tooltron 
  by RFID lookup but not authorized to use specific tool
  outside scope of original RFID lookup request).
  """
  success = models.BooleanField(default=True)

  """
  Project editable field.
  Extra endpoint and request specific information.
  """
  meta = models.TextField(null=True)

  def __str__(self):
    return self.endpoint
