from django.contrib import admin
from django.core import urlresolvers

class UpdatedByAdmin(admin.ModelAdmin):

  def save_model(self, request, obj, form, change):
    obj.updater_object = request.user
    obj.save()

  def updater_url(self, obj):

    # RoboUsers have no change url
    if type(obj.updater_object).__name__ == 'RoboUser':
      obj.updater_object = obj.updater_object.user

    s = "admin:{}_{}_change".format(obj.updater_type.app_label, obj.updater_type.model)
    url = urlresolvers.reverse(s, args=(obj.updater_id, ))
    return '<a href="{}">{}</a>'.format(url, obj.updater_object)
  updater_url.allow_tags = True
  updater_url.short_description = "Updater"
