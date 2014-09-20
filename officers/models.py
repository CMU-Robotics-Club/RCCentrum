from django.db import models
from django.conf import settings
from ordered_model.models import OrderedModel

class Officer(OrderedModel):

  position = models.CharField(max_length=30)

  user = models.ForeignKey('robocrm.RoboUser')

  def image_upload_to(instance, filename):
    print(filename)
    #TODO: name file project name
    #return "projects/{}".format(instance.name)
    return "officers/{}".format(filename)

  image = models.ImageField(upload_to=image_upload_to, null=True)

  description = models.TextField(null=True)

  class Meta(OrderedModel.Meta):
    pass

  # To show image in admin interface
  def current_image(self, width=100, height=100):
    return '<img src="{}{}" width="{}px" height="{}px" class="img-responsive img-thumbnail"/>'.format(settings.MEDIA_URL, self.image, width, height)
  current_image.allow_tags = True

  def __str__(self):
    return self.position