from django.db import models
from ordered_model.models import OrderedModel
from easy_thumbnails.fields import ThumbnailerImageField

class Photo(OrderedModel):

  title = models.CharField(max_length=30, null=True, blank=True)

  description = models.TextField(null=True, blank=True)

  def image_upload_to(instance, filename):
    return "gallery/{}".format(filename)

  image = ThumbnailerImageField(upload_to=image_upload_to)

  """
  If this photo should be displayed in front page gallery.
  """
  display = models.BooleanField(default=False)

  def __str__(self):
    return str(self.id)
