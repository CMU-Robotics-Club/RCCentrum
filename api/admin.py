from django.contrib import admin
from django.core import urlresolvers
from .models import APIRequest
from crm.admin import UpdatedByAdmin

_fields = ('id', 'endpoint', 'project', 'user_url', 'created_datetime', 'updated_datetime', 'success', 'meta', )

class APIRequestAdmin(UpdatedByAdmin):
  fields = _fields
  readonly_fields = _fields
  list_display = _fields

  # Only Projects should/can access API endpoints 
  # that are logged and thus give this field a less
  # confusing name of "Project"
  def project(self, obj):
    return self.updater_url(obj)
  project.allow_tags = True

  def user_url(self, obj):
    if obj.user:
      url = urlresolvers.reverse("admin:auth_user_change", args=(obj.user.id, ))
      return '<a href="{}">{}</a>'.format(url, obj.user)
    else:
      return ''
  user_url.allow_tags = True
  user_url.short_description = "User"

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