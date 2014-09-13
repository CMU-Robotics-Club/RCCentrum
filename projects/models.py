from django.db import models
from django.conf import settings

# TODO: move to seperate project app
class Project(models.Model):
  name = models.CharField(max_length=30)

  def image_upload_to(instance, filename):
    print(filename)
    #TODO: name file project name
    #return "projects/{}".format(instance.name)
    return "projects/{}".format(filename)

  image = models.ImageField(upload_to=image_upload_to, null=True)

  # What is displayed on project overview page
  blurb = models.TextField(null=True)
  # Full description
  description = models.TextField(null=True)

  website = models.URLField(null=True)

  leaders = models.ManyToManyField('robocrm.RoboUser', related_name='u+')

  # To show image in admin interface
  def current_image(self):
    return '<img src="{}{}" width="100px height=100px"/>'.format(settings.MEDIA_URL, self.image)
  current_image.allow_tags = True

  def __str__(self):
    return self.name