from django.contrib import admin
from .models import UPCItem

class UPCItemAdmin(admin.ModelAdmin):
  fields = ('name', 'upc', 'cost', )
  list_display = ('name', 'upc', 'cost', )
  readonly_fields = ('upc', )

  def get_readonly_fields(self, request, obj=None):
    user = request.user

    if not user.is_superuser and not user.groups.filter(name='officers').exists():
      return super().get_readonly_fields(request, obj) + ('name', 'cost', )
    else:
      return super().get_readonly_fields(request, obj)


  # No one should be able to add, change, or remove UPCItem information
  def has_add_permission(self, request):
    return False

  def has_delete_permission(self, request, obj=None):
    return False

  def get_actions(self, request):
    actions = super().get_actions(request)
    del actions['delete_selected']
    return actions


admin.site.register(UPCItem, UPCItemAdmin)
