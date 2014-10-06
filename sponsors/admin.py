from django.contrib import admin
from .models import Sponsor
from ordered_model.admin import OrderedModelAdmin

class SponsorAdmin(OrderedModelAdmin):
  fields = ('name', 'current_logo', 'logo', 'website', 'active', )
  readonly_fields = ['current_logo']
  list_display = ('name', 'website', 'move_up_down_links', )

admin.site.register(Sponsor, SponsorAdmin)