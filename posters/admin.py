from django.contrib import admin
from .models import Poster

class PosterAdmin(admin.ModelAdmin):
  fields = ('name', 'year', 'current_image', 'image', )
  readonly_fields = ['current_image']
  list_display = ('name', 'current_image', 'year', )
  list_filter = ('name', 'year', )

admin.site.register(Poster, PosterAdmin)