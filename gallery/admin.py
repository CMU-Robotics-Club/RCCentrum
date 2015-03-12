from django.contrib import admin
from django.utils.safestring import mark_safe
from ordered_model.admin import OrderedModelAdmin
from tinymce.widgets import TinyMCE
from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):
  
  description = forms.CharField(widget=TinyMCE(attrs={'cols': 160, 'rows': 10}), required=False)

  class Meta:
    model = Photo
    exclude = ()


class PhotoAdmin(OrderedModelAdmin):
  
  form = PhotoForm

  list_display = ('id', 'title', 'description_safe', 'display', 'current_image', 'move_up_down_links', )
  fields = ('id', 'title', 'description', 'display', 'image', 'current_image', )
  readonly_fields = ('id', 'current_image', )

  def description_safe(self, obj):
    return mark_safe(obj.description)
  description_safe.short_description = 'Description'

  def current_image(self, obj):
    return mark_safe('<a href="{}"><img src="{}" /></a>'.format(obj.image.url, obj.image['poster_admin'].url))

admin.site.register(Photo, PhotoAdmin)
