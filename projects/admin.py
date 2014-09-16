from django.contrib import admin
from projects.models import Project

class ProjectAdmin(admin.ModelAdmin):
  fields = ('name', 'current_image', 'image', 'blurb', 'description', 'website', 'leaders', 'display', 'last_api_activity')
  readonly_fields = ['current_image', 'last_api_activity']

admin.site.register(Project, ProjectAdmin)