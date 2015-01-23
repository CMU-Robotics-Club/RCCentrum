from django.contrib import admin
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType

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


class UpdatedByListFilter(admin.SimpleListFilter):
  """
  Filter by existing APIRequest updater_objects.
  """

  title = ('Updater')
  parameter_name = 'updater'

  def lookups(self, request, model_admin):
    updaters = set()
      
    # Put in set to avoid duplicates
    for api_request in model_admin.model.objects.all():
      updater = api_request.updater_object
      updaters.add(updater)
      
    results = []

    # Extract unique updater_objects
    # and store Content Type ID and Content ID in URL
    for updater in list(updaters):
      results.append(("{} {}".format(ContentType.objects.get_for_model(updater).id, updater.id), updater))

    return results

  def queryset(self, request, queryset):
    if(self.value()):
      # Extract Content Type ID and Content ID from URL
      content_type_id, object_id = self.value().split()

      content_type = ContentType.objects.get(id=content_type_id)
      updater = content_type.get_object_for_this_type(id=object_id)
        
      return queryset.filter(updater_type=content_type).filter(updater_id=updater.id)
    else:
      return queryset
