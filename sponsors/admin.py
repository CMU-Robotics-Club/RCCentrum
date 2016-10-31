from django.contrib import admin
from .models import Sponsor
from ordered_model.admin import OrderedModelAdmin
from django.utils.safestring import mark_safe

class SponsorAdmin(OrderedModelAdmin):
  fields = ('name', 'current_logo', 'logo', 'website', 'active', 'description', )
  readonly_fields = ['current_logo']
  list_display = ('name', 'current_logo', 'active', 'website_safe', 'move_up_down_links', )
  list_filter = ('active', )

  def website_safe(self, obj):
    return mark_safe("<a href={0}>{0}</a>".format(obj.website))
  website_safe.short_description = 'Website'

admin.site.register(Sponsor, SponsorAdmin)
