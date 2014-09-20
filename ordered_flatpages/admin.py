from django.contrib import admin
from django import forms
from django.contrib.flatpages.models import FlatPage
from .models import OrderedFlatPage
from tinymce.widgets import TinyMCE
from ordered_model.admin import OrderedModelAdmin

class OrderedFlatPageForm(forms.ModelForm):
  
  content = forms.CharField(widget=TinyMCE(attrs={'cols': 160, 'rows': 60}))

  class Meta:
    model = OrderedFlatPage
    exclude = ('template_name', 'registration_required', 'enable_comments', )

class OrderedFlatPageAdmin(OrderedModelAdmin):
  form = OrderedFlatPageForm

  list_display = ('title', 'url', 'move_up_down_links', )

admin.site.unregister(FlatPage)
admin.site.register(OrderedFlatPage, OrderedFlatPageAdmin)