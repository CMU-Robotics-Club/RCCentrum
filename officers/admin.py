from django.contrib import admin
from .models import Officer
from ordered_model.admin import OrderedModelAdmin

class OfficerAdmin(OrderedModelAdmin):
  fields = ('position', 'user', 'current_image', 'image', 'memo', 'description', )
  readonly_fields = ['current_image']
  list_display = ('user', 'current_image', 'position', 'memo', 'description', 'move_up_down_links', )

admin.site.register(Officer, OfficerAdmin)
