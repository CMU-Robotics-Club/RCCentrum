from django.contrib import admin
from .models import Link
from ordered_model.admin import OrderedModelAdmin

class LinkAdmin(OrderedModelAdmin):
  fields = ('name', 'url', )
  list_display = ('name', 'url', 'move_up_down_links', )

admin.site.register(Link, LinkAdmin)