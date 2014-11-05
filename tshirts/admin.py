from django.contrib import admin
from .models import TShirt
from ordered_model.admin import OrderedModelAdmin

class TShirtAdmin(OrderedModelAdmin):
  fields = ('name', 'year', 'current_front_image', 'front_image', 'current_back_image', 'back_image' )
  readonly_fields = ['current_front_image', 'current_back_image']
  list_display = ('name', 'year', 'current_front_image', 'current_back_image', )

admin.site.register(TShirt, TShirtAdmin)