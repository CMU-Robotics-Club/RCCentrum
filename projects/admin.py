from django.contrib import admin
from projects.models import Project

class ProjectAdmin(admin.ModelAdmin):

  fields = ('name', 'current_image', 'image', 'blurb', 'description', 'website', 'leaders', 'display', 'private_key', 'last_api_activity')
  filter_horizontal = ('leaders',)
  readonly_fields = ['current_image', 'last_api_activity']
  list_display = ('name', 'current_image', 'website', 'display', 'blurb', 'last_api_activity')

  # TODO: find be a better way to do this function
  def get_form(self, request, obj=None, **kwargs):
    user = request.user

    if not user.is_superuser and not user.groups.filter(name='officers').exists():      
      if 'display' not in self.readonly_fields:
        self.readonly_fields.append('display')
    else:
      if 'display' in self.readonly_fields:
        self.readonly_fields.remove('display')

    return super().get_form(request, obj, **kwargs)

  def get_queryset(self, request):
    qs = super().get_queryset(request)

    user = request.user

    # If not an superuser/officer only
    # let Robouser admin projects a leader of
    if not user.is_superuser and not user.groups.filter(name='officers').exists():
      # Get the robouser so the IDs match up
      robouser = user.robouser
      qs = qs.filter(leaders=robouser.id)

    return qs

admin.site.register(Project, ProjectAdmin)