from django.db import models

class Webcam(models.Model):

  name = models.CharField(max_length=10)
  url = models.URLField()

  def __str__(self):
    return self.name