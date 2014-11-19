from django.contrib import admin
from .models import Channel

class ChannelAdmin(admin.ModelAdmin):
  fields = ('id', 'name', 'value', 'created', 'updated', 'active', )
  readonly_fields = ['id', 'created', 'updated', 'active', ]
  list_display = ('id', 'name', 'value', 'created', 'updated', 'active', )

  def get_readonly_fields(self, request, obj=None):
    if obj:
      return super().get_readonly_fields(request, obj) + ['name']
    else:
      return super().get_readonly_fields(request, obj)

admin.site.register(Channel, ChannelAdmin)