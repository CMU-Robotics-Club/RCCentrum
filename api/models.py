from django.db import models
from crm.models import UpdatedByModel

class APIRequest(UpdatedByModel):
  """
  Log of API Requests for /rfid/, /magnetic/,
  /users/:id/email/, and /users/:id/rfid/
  since these are considered 'sensitive' or
  'priveleged' endpoints.
  """

  """
  Not project editable.
  Name of the request endpoint.
  """
  endpoint = models.CharField(max_length=30, editable=False)
  
  """
  Not project editable.
  Extra information provided by endpoint view.
  """
  extra = models.TextField(null=True, editable=False)

  """
  Not project editable.
  Which RoboUser this request is for.
  (Can be none if invalid request)
  """
  user = models.ForeignKey('robocrm.RoboUser', null=True, editable=False)
  
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

  """
  Not Project editable.
  The value of the HTTP Header 'API_CLIENT' if present.
  """
  api_client = models.CharField(max_length=50, null=True, editable=False)

  def __str__(self):
    return self.endpoint
