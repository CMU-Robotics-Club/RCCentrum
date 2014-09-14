from django.contrib import admin
from .models import Officer

class OfficerAdmin(admin.ModelAdmin):
  fields = ('position', 'user', 'current_image', 'image', 'description', )
  readonly_fields = ['current_image']

admin.site.register(Officer, OfficerAdmin)
