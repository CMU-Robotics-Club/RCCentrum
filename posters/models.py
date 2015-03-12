from django.db import models
from django.conf import settings
import os
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer
from django.utils.safestring import mark_safe

class Poster(models.Model):

  name = models.CharField(max_length=100)

  year = models.PositiveIntegerField()

  def image_upload_to(instance, filename):
    filename, extension = os.path.splitext(filename)
    name = instance.name
    return "posters/{}{}".format(name, extension)

  image = ThumbnailerImageField(upload_to=image_upload_to)

  class Meta:
    ordering = ['year', 'name', ]

  # To show image in admin interface
  def current_image(self, width=100, height=100):
    return mark_safe('<a href="{}"><img src="{}" /></a>'.format(self.image.url, self.image['poster_admin'].url))

  def __str__(self):
    return self.name
