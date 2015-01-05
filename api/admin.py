from django.contrib import admin
from django.core import urlresolvers
from .models import APIRequest
from crm.admin import UpdatedByAdmin

_fields = ('id', 'endpoint', 'extra', 'requester', 'user_url', 'created_datetime', 'updated_datetime', 'success', 'meta', 'api_client', )

class APIRequestAdmin(UpdatedByAdmin):

  change_form_template = "admin/change_form_no_change_save.html"

  fields = _fields
  readonly_fields = _fields
  list_display = _fields

  def requester(self, obj):
    return self.updater_url(obj)
  requester.allow_tags = True

  def user_url(self, obj):
    if obj.user:
      url = urlresolvers.reverse("admin:auth_user_change", args=(obj.user.user.id, ))
      return '<a href="{}">{}</a>'.format(url, obj.user.user)
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

admin.site.register(APIRequest, APIRequestAdmin)