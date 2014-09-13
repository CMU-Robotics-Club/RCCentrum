from django.contrib import admin
from projects.models import Project

class ProjectAdmin(admin.ModelAdmin):
  #list_display = ('name', 'project_image', 'image', 'blurb', 'description', 'website')
  fields = ('name', 'current_image', 'image', 'blurb', 'description', 'website', 'leaders')
  readonly_fields = ['current_image']
  #list_display = ('thumb', 'rentitem', 'is_avatar', 'description')

admin.site.register(Project, ProjectAdmin)