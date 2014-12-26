from django.contrib import admin
from .models import Officer
from ordered_model.admin import OrderedModelAdmin
from django_object_actions import DjangoObjectActions
from django.http import HttpResponse
from .label import create_officer_label

class OfficerAdmin(DjangoObjectActions, OrderedModelAdmin):
  fields = ('position', 'user', 'current_image', 'image', 'memo', 'description', )
  readonly_fields = ['current_image']
  list_display = ('user', 'current_image', 'position', 'memo', 'description', 'move_up_down_links', )

  def create_officer_label(self, request, obj):
    response = HttpResponse(content_type="image/png")
    image = create_officer_label(obj)
    image.save(response, "PNG")
    return response
  create_officer_label.label = "<i class='icon-picture icon-alpha75'></i>Create Officer Label"

  objectactions = ('create_officer_label', )

admin.site.register(Officer, OfficerAdmin)
