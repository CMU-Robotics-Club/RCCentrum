from django.contrib import admin
from .models import Quote

class QuoteAdmin(admin.ModelAdmin):
  fields = ('quote', )
  list_display = ('id', 'quote', )

  # Hides admin interface from Admin sidebar
  # Users can still visit the Admin Model URL
  # directly
  def get_model_perms(self, request):
    return {}

admin.site.register(Quote, QuoteAdmin)