from django.contrib import admin
from django import forms
from tinymce.widgets import TinyMCE
from .models import Channel
from crm.admin import UpdatedByAdmin

class ChannelForm(forms.ModelForm):
  
  description = forms.CharField(widget=TinyMCE(attrs={'cols': 160, 'rows': 10}))

  class Meta:
    model = Channel
    exclude = ()


class ChannelAdmin(UpdatedByAdmin):

  fields = ('id', 'name', 'value', 'created_datetime', 'updated_datetime', 'updater_url', 'description', )
  readonly_fields = ['id', 'created_datetime', 'updated_datetime', 'updater_url', ]
  list_display = ('id', 'name', 'value', 'created_datetime', 'updated_datetime', 'updater_url', 'description_html', )
  form = ChannelForm

  # So description can be HTML rendered
  def description_html(self, obj):
    return obj.description
  description_html.short_description = "Description"
  description_html.allow_tags = True

  def get_readonly_fields(self, request, obj=None):
    if obj:
      return super().get_readonly_fields(request, obj) + ['name']
    else:
      return super().get_readonly_fields(request, obj)


admin.site.register(Channel, ChannelAdmin)