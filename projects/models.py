from django.db import models
from django.conf import settings
import os

class Project(models.Model):
  name = models.CharField(max_length=30)

  def image_upload_to(instance, filename):
    name, extension = os.path.splitext(filename)
    return "projects/{}{}".format(instance.name.lower(), extension)

  image = models.ImageField(upload_to=image_upload_to, null=True)

  # What is displayed on project overview page
  blurb = models.TextField(null=True)
  # Full description
  description = models.TextField(null=True)

  website = models.URLField(null=True)

  leaders = models.ManyToManyField('robocrm.RoboUser', related_name='u+')

  # Display on website
  display = models.BooleanField(default=False)

  last_api_activity = models.DateTimeField(null=True)

  # To show image in admin interface
  def current_image(self):
    return '<img src="{}{}" width="100px height=100px"/>'.format(settings.MEDIA_URL, self.image)
  current_image.allow_tags = True

  def __str__(self):
    return self.name
