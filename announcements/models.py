from django.db import models
from crm.models import UpdatedByModel

class Announcement(UpdatedByModel):
  """
  RoboClub announcements that can be digitally
  distributed or physically printed for the club/school
  by creating a announcement label from the admin interface.
  """

  header = models.TextField(null=True)
  body = models.TextField(null=True)
