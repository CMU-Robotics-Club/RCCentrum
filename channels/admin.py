from django.contrib import admin
from .models import Channel
from crm.admin import UpdatedByAdmin

class ChannelAdmin(UpdatedByAdmin):

  fields = ('id', 'name', 'value', 'created_datetime', 'updated_datetime', 'updater_url', 'description', )
  readonly_fields = ['id', 'created_datetime', 'updated_datetime', 'updater_url', ]
  list_display = ('id', 'name', 'value', 'created_datetime', 'updated_datetime', 'updater_url', 'description', )

  def get_readonly_fields(self, request, obj=None):
    if obj:
      return super().get_readonly_fields(request, obj) + ['name']
    else:
      return super().get_readonly_fields(request, obj)

admin.site.register(Channel, ChannelAdmin)