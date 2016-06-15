from django.contrib import admin
from .models import Announcement
from crm.admin import UpdatedByAdmin
from django_object_actions import DjangoObjectActions
from django.http import HttpResponse
from .label import create_announcement_label

class AnnouncementAdmin(DjangoObjectActions, UpdatedByAdmin):
  
  fields = ('id', 'header', 'body', 'created_datetime', 'updated_datetime', 'updater_url', )
  readonly_fields = ['id', 'created_datetime', 'updated_datetime', 'updater_url', ]
  list_display = ('id', 'header', 'body', 'created_datetime', 'updated_datetime', 'updater_url', )

  def create_announcement_label(self, request, obj):
    response = HttpResponse(content_type="image/png")
    image = create_announcement_label(obj)
    image.save(response, "PNG")
    return response
  create_announcement_label.label = "<i class='icon-picture icon-alpha75'></i>Create Announcement Label"

  objectactions = ('create_announcement_label', )

admin.site.register(Announcement, AnnouncementAdmin)

