from django.db import models
from django.conf import settings
import os
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import random
import string
from robocrm.models import RoboUser

class Project(models.Model):
  name = models.CharField(max_length=30, unique=True)

  def image_upload_to(instance, filename):
    name, extension = os.path.splitext(filename)
    return "projects/{}{}".format(instance.name.lower(), extension)

  def clean(self):
    if len(self.private_key) == 0:
      self.private_key = ''.join(random.choice(string.hexdigits) for i in range(30))

    if len(self.private_key) < 30:
      raise ValidationError("PrivateKey must be at least 30 characters")

    super().clean()

  image = models.ImageField(upload_to=image_upload_to, null=True, default='logo.png')

  # What is displayed on project overview page
  blurb = models.TextField(null=True, help_text="Miniature description displayed on project overview page.")
  # Full description
  description = models.TextField(null=True, blank=True, help_text="Full description displayed on project detail page.")

  website = models.URLField(null=True, blank=True)

  leaders = models.ManyToManyField('robocrm.RoboUser', related_name='u+')

  # Display on website
  display = models.BooleanField(default=False)

  last_api_activity = models.DateTimeField(null=True)

  # To show image in admin interface
  def current_image(self):
    return '<img src="{}{}" width="100px height=100px"/>'.format(settings.MEDIA_URL, self.image)
  current_image.allow_tags = True

  private_key = models.CharField(max_length=50)

  def __str__(self):
    return self.name
