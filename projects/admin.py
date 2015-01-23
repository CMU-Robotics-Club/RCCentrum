from django.contrib import admin
from projects.models import Project
from robocrm.models import RoboUser
from django.forms import ModelForm, CharField
from django_object_actions import DjangoObjectActions
from django.conf import settings
from django.http import HttpResponse
from projects.label import create_project_label
from tinymce.widgets import TinyMCE

class ProjectCreationForm(ModelForm):

  def save(self, commit=True):
    project = super().save(commit=False)

    # Hacky but only way to get default leaders to work since
    # original save_m2m overrides groups
    old_save_m2m = self.save_m2m
    def save_m2m():
      old_save_m2m()
      project.leaders.clear()

      if hasattr(self.user, 'robouser'):
        project.leaders.add(self.user.robouser)
    self.save_m2m = save_m2m

    if commit:
      project.save()

    return project

  class Meta:
    model = Project
    fields = ('name', 'image', 'blurb', 'description', 'website', )


class ProjectForm(ModelForm):
  
  blurb = CharField(widget=TinyMCE(attrs={'cols': 160, 'rows': 20}))
  description = CharField(widget=TinyMCE(attrs={'cols': 160, 'rows': 20}))

  class Meta:
    model = Project
    exclude = ()


class ProjectAdmin(DjangoObjectActions, admin.ModelAdmin):

  fields = ('name', 'current_image', 'image', 'blurb', 'description', 'website', 'leaders', 'display', 'private_key', 'last_api_activity')
  filter_horizontal = ('leaders',)
  readonly_fields = ['current_image', 'last_api_activity']
  list_display = ('name', 'current_image', 'website', 'display', 'blurb', 'last_api_activity')
  list_filter = ('display', )
  form = ProjectForm

  def create_project_label(self, request, obj):
    response = HttpResponse(content_type="image/png")
    image = create_project_label(obj)
    image.save(response, "PNG")
    return response
  create_project_label.label = "<i class='icon-picture icon-alpha75'></i>Create Project Label"

  objectactions = ('create_project_label', )

  def get_form(self, request, obj=None, **kwargs):
    if obj:
      return super().get_form(request, obj, **kwargs)
    else:
      form = ProjectCreationForm
      form.user = request.user
      return form

  def get_readonly_fields(self, request, obj=None):
    user = request.user

    if not user.is_superuser and not user.groups.filter(name='officers').exists():
      return super().get_readonly_fields(request, obj) + ['display']
    else:
      return super().get_readonly_fields(request, obj)

  def get_fieldsets(self, request, obj=None):
    if obj:
      return super().get_fieldsets(request, obj)
    else:
      # add user form
      return (
          (None, {'fields':
            ('name', 'image', 'blurb', 'description', 'website',
            )
          }),)

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