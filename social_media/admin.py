from django.contrib import admin
from .models import SocialMedia
from ordered_model.admin import OrderedModelAdmin

class SocialMediaAdmin(OrderedModelAdmin):
  fields = ('name', 'url', )
  list_display = ('name', 'url', 'move_up_down_links', )

admin.site.register(SocialMedia, SocialMediaAdmin)