from django.contrib import admin
from .models import Webcam
from ordered_model.admin import OrderedModelAdmin

class WebcamAdmin(OrderedModelAdmin):
  list_display = ('name', 'url', 'move_up_down_links', )

admin.site.register(Webcam, WebcamAdmin)