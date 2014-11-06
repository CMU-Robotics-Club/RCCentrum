from django.db import models
from django.conf import settings
from ordered_model.models import OrderedModel
import os

class Poster(OrderedModel):

  name = models.CharField(max_length=30, unique=True)

  year = models.PositiveIntegerField()

  def image_upload_to(instance, filename):
    filename, extension = os.path.splitext(filename)
    name = instance.name
    return "posters/{}{}".format(name, extension)

  image = models.ImageField(upload_to=image_upload_to)

  class Meta(OrderedModel.Meta):
    pass

  # To show image in admin interface
  def current_image(self, width=100, height=100):
    return '<img src="{}{}" width="{}px" height="{}px" class="img-responsive img-thumbnail"/>'.format(settings.MEDIA_URL, self.image, width, height)
  current_image.allow_tags = True

  def __str__(self):
    return self.name
