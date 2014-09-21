from django.db import models
from ordered_model.models import OrderedModel

class Webcam(OrderedModel):

  name = models.CharField(max_length=10)
  url = models.URLField()

  class Meta(OrderedModel.Meta):
    pass

  def __str__(self):
    return self.name