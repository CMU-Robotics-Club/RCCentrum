from django.db import models
from ordered_model.models import OrderedModel

class Category(OrderedModel):
  title = models.CharField(max_length=30)

  class Meta(OrderedModel.Meta):
    verbose_name_plural = 'Categories'

class QA(OrderedModel):
  category = models.ForeignKey(Category)
  question = models.TextField()
  answer = models.TextField()

  class Meta(OrderedModel.Meta):
    verbose_name_plural = 'QAs'
