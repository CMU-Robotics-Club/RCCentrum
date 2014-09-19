from rest_framework import authentication
from rest_framework import exceptions
from projects.models import Project
from django.utils import timezone
from .errno import *

class RCAuthentication(authentication.BaseAuthentication):

  def authenticate(self, request):
    project_id = request.META.get('HTTP_X_PROJECT_ID')
    project_name = request.META.get('HTTP_X_PROJECT_NAME')

    if not project_id or not project_name:
      e = exceptions.AuthenticationFailed(detail='Invalid authentication credentials')
      e.errno = INVALID_PROJECT_AUTHENTICATION
      raise e

    try:
      project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
      e = exceptions.AuthenticationFailed(detail='Invalid authentication credentials')
      e.errno = INVALID_PROJECT_AUTHENTICATION
      raise e

    if project.name != project_name:
      e = exceptions.AuthenticationFailed(detail='Invalid authentication credentials')
      e.errno = INVALID_PROJECT_AUTHENTICATION
      raise e

    # Hacky solution so django-rest-framework does not through exception
    project.is_authenticated = lambda : True
    project.last_api_activity = timezone.now()
    project.save()

    return (project, None)
