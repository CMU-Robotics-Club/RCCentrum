from django.contrib import admin
from django.core import urlresolvers
from .models import APIRequest

_fields = ('id', 'endpoint', 'requester_url', 'user_url', 'meta', 'created_date', 'modified_date', )

class APIRequestAdmin(admin.ModelAdmin):
  fields = _fields
  readonly_fields = _fields
  list_display = _fields

  def requester_url(self, obj):
    s = "admin:{}_{}_change".format(obj.requester_type.app_label, obj.requester_type.model)
    url = urlresolvers.reverse(s, args=(obj.requester_id, ))
    return '<a href="{}">{}</a>'.format(url, obj.requester_object)
  requester_url.allow_tags = True
  requester_url.short_description = "Requester"

  def user_url(self, obj):
    if obj.user:
      url = urlresolvers.reverse("admin:auth_user_change", args=(obj.user.id, ))
      return '<a href="{}">{}</a>'.format(url, obj.user)
    else:
      return ''
  user_url.allow_tags = True
  user_url.short_description = "User Lookup"

  # No one should be able to add, change, or remove API log information
  def has_add_permission(self, request):
    return False

  def has_delete_permission(self, request, obj=None):
    return False

  def get_actions(self, request):
    actions = super().get_actions(request)
    del actions['delete_selected']
    return actions

  class Media:
    # Hacky way to hide the "Save"
    # and "Save and Add Another" buttons
    # but is the only solution that appears to work.
    js = ('/static/hide_save.js',)

admin.site.register(APIRequest, APIRequestAdmin)