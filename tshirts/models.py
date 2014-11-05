from django.db import models
from django.utils import timezone
from django.conf import settings
import os

class TShirt(models.Model):

  name = models.CharField(max_length=30, unique=True)

  year = models.PositiveIntegerField()

  def front_image_upload_to(instance, filename):
    filename, extension = os.path.splitext(filename)
    year = instance.year
    return "tshirts/{}_front{}".format(year, extension)

  def back_image_upload_to(instance, filename):
    filename, extension = os.path.splitext(filename)
    year = instance.year
    return "tshirts/{}_back{}".format(year, extension)

  front_image = models.ImageField(upload_to=front_image_upload_to)
  back_image = models.ImageField(upload_to=back_image_upload_to)

  # TODO: make base model class than contain 
  # images with upload and curret_image functions
  # To show image in admin interface
  def current_front_image(self, width=100, height=100):
    return '<img src="{}{}" width="{}px" height="{}px" class="img-responsive img-thumbnail"/>'.format(settings.MEDIA_URL, self.front_image, width, height)
  current_front_image.allow_tags = True

  def current_back_image(self, width=100, height=100):
    return '<img src="{}{}" width="{}px" height="{}px" class="img-responsive img-thumbnail"/>'.format(settings.MEDIA_URL, self.back_image, width, height)
  current_back_image.allow_tags = True

  class Meta:
    ordering = ['year', 'name', ]

  def __str__(self):
    return self.name
