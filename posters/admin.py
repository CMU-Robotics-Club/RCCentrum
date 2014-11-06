from django.contrib import admin
from .models import Poster
from django.utils.safestring import mark_safe

class PosterAdmin(admin.ModelAdmin):
  fields = ('name', 'year', 'current_image', 'image', )
  readonly_fields = ['current_image']
  list_display = ('name', 'current_image', 'year', )

admin.site.register(Poster, PosterAdmin)