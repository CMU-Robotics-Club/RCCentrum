from django.contrib import admin
from projects.models import Project

class ProjectAdmin(admin.ModelAdmin):
  fields = ('name', 'current_image', 'image', 'blurb', 'description', 'website', 'leaders', 'display')
  readonly_fields = ['current_image']

admin.site.register(Project, ProjectAdmin)