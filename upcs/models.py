from django.db import models

class UPCItem(models.Model):

  name = models.CharField(max_length=50)

  upc = models.CharField(max_length=12, unique=True)
  
  cost = models.DecimalField(
    max_digits=5,
    decimal_places=2,
    default=0.50,
  )

  def __str__(self):
    return self.name