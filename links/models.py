from django.db import models
from ordered_model.models import OrderedModel

class Link(OrderedModel):

  name = models.CharField(max_length=30)
  url = models.URLField()

  class Meta(OrderedModel.Meta):
    pass

  def __str__(self):
    return self.name