from django.db import models
from django.conf import settings
import os
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import random
import string
from django.utils.safestring import mark_safe

def create_private_key():
  return ''.join(random.choice(string.hexdigits) for i in range(40))


class Project(models.Model):
  name = models.CharField(max_length=30, unique=True)

  def image_upload_to(instance, filename):
    name, extension = os.path.splitext(filename)
    return "projects/{}{}".format(instance.name.lower(), extension)

  def clean(self):
    if len(self.private_key) < settings.PROJECT_PRIVATE_KEY_MIN_LENGTH:
      raise ValidationError("Private Key must be at least {} characters".format(settings.PROJECT_PRIVATE_KEY_MIN_LENGTH))

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
    return mark_safe('<img src="{}{}" width="100px height=100px"/>'.format(settings.MEDIA_URL, self.image))

  private_key = models.CharField(max_length=50, default=create_private_key)

  def __str__(self):
    return self.name
