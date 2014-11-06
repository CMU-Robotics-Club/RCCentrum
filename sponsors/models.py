from django.db import models
from django.conf import settings
from ordered_model.models import OrderedModel
import os

class Sponsor(OrderedModel):
  name = models.CharField(max_length=30, unique=True)

  def image_upload_to(instance, filename):
    name, extension = os.path.splitext(filename)
    name = instance.name
    return "sponsors/{}{}".format(name, extension)

  logo = models.ImageField(upload_to=image_upload_to, null=True)

  website = models.URLField(null=True)

  active = models.BooleanField(default=False)

  # To show image in admin interface
  def current_logo(self, width=100, height=100):
    return '<img src="{}{}" width="{}px" height="{}px" class="img-responsive img-thumbnail"/>'.format(settings.MEDIA_URL, self.logo, width, height)
  current_logo.allow_tags = True

  def __str__(self):
    return self.name
