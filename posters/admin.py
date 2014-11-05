from django.contrib import admin
from .models import Poster
from ordered_model.admin import OrderedModelAdmin

class PosterAdmin(OrderedModelAdmin):
  fields = ('name', 'year', 'current_image', 'image', )
  readonly_fields = ['current_image']
  list_display = ('name', 'current_image', 'year', 'move_up_down_links', )

admin.site.register(Poster, PosterAdmin)