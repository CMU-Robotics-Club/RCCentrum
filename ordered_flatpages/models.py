from django.db import models
from django.contrib.flatpages.models import FlatPage
from ordered_model.models import OrderedModel

class OrderedFlatPage(FlatPage, OrderedModel):
  
  class Meta(OrderedModel.Meta):
    pass
