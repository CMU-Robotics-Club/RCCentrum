from django.contrib import admin
from .models import Webcam
from ordered_model.admin import OrderedModelAdmin
from django.utils.safestring import mark_safe

class WebcamAdmin(OrderedModelAdmin):
  list_display = ('name', 'url_safe', 'move_up_down_links', )

  def url_safe(self, obj):
    return mark_safe("<a href={0}>{0}</a>".format(obj.url))

  url_safe.short_description = 'URL'

admin.site.register(Webcam, WebcamAdmin)