from django.db import models
from ordered_model.models import OrderedModel

class SocialMedia(OrderedModel):
  name = models.CharField(max_length=30)
  url = models.URLField(null=True)

  def __str__(self):
    return self.name
