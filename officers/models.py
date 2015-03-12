from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from ordered_model.models import OrderedModel
import os

class Officer(OrderedModel):

  position = models.CharField(max_length=30)

  user = models.ForeignKey('robocrm.RoboUser')

  def image_upload_to(instance, filename):
    name, extension = os.path.splitext(filename)
    username = instance.user.user.username
    return "officers/{}{}".format(username, extension)

  image = models.ImageField(upload_to=image_upload_to, null=True)

  memo = models.TextField(null=True)
  
  description = models.TextField(null=True)

  class Meta(OrderedModel.Meta):
    pass

  # To show image in admin interface
  def current_image(self, width=100, height=100):
    return mark_safe('<img src="{}{}" width="{}px" height="{}px" class="img-responsive img-thumbnail"/>'.format(settings.MEDIA_URL, self.image, width, height))

  def __str__(self):
    return self.position