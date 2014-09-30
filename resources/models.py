from django.db import models

class Resource(models.Model):
  
  resource = models.FileField(upload_to='uploads/')

  def __str__(self):
    return str(self.resource)
