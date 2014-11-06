from django.db import models
from django.conf import settings
import os

class Poster(models.Model):

  name = models.CharField(max_length=100)

  year = models.PositiveIntegerField()

  def image_upload_to(instance, filename):
    filename, extension = os.path.splitext(filename)
    name = instance.name
    return "posters/{}{}".format(name, extension)

  image = models.ImageField(upload_to=image_upload_to)

  class Meta:
    ordering = ['year', 'name', ]

  # To show image in admin interface
  def current_image(self, width=100, height=100):
    return '<a href="{0}{1}"><img src="{0}{1}" width="{2}px" height="{2}px" class="img-responsive img-thumbnail"/></a>'.format(settings.MEDIA_URL, self.image, width, height)
  current_image.allow_tags = True

  def __str__(self):
    return self.name
