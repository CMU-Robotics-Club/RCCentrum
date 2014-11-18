from django.contrib import admin
from .models import Channel

class ChannelAdmin(admin.ModelAdmin):
  fields = ('id', 'name', 'value', 'created', 'updated', 'active', )
  readonly_fields = ['id', 'name', 'created', 'updated', 'active', ]
  list_display = ('id', 'name', 'value', 'created', 'updated', 'active', )

admin.site.register(Channel, ChannelAdmin)