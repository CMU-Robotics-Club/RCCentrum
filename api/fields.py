from rest_framework import serializers
from django.conf import settings
from django.contrib.sites.models import Site

class APIImageField(serializers.ImageField):

  def to_native(self, obj):
    parent = super(APIImageField, self).to_native(obj)
    site = Site.objects.get_current()
    url = "{}{}/{}".format(site.domain, settings.MEDIA_URL, parent)
    return url
    