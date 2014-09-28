from django.contrib import admin
from projects.models import Project

class ProjectAdmin(admin.ModelAdmin):
  fields = ('name', 'current_image', 'image', 'blurb', 'description', 'website', 'leaders', 'display', 'last_api_activity')
  readonly_fields = ['current_image', 'last_api_activity']

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