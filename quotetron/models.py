from django.db import models

class Quote(models.Model):
  quote = models.TextField()

  def __str__(self):
    return self.quote
