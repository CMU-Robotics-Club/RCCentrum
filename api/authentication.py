from rest_framework import authentication
from rest_framework import exceptions
from projects.models import Project
from django.utils import timezone
from .errno import *

class RCAuthentication(authentication.BaseAuthentication):

  def authenticate(self, request):
    public = request.META.get('HTTP_PUBLIC_KEY')
    private = request.META.get('HTTP_PRIVATE_KEY')

    if not public or not private:
      e = exceptions.AuthenticationFailed(detail='Invalid authentication credentials')
      e.errno = INVALID_PROJECT_AUTHENTICATION
      raise e

    try:
      public = int(public)
    except ValueError:
      e = exceptions.AuthenticationFailed(detail='Invalid authentication credentials')
      e.errno = INVALID_PROJECT_AUTHENTICATION
      raise e

    try:
      project = Project.objects.get(id=public)
    except Project.DoesNotExist:
      e = exceptions.AuthenticationFailed(detail='Invalid authentication credentials')
      e.errno = INVALID_PROJECT_AUTHENTICATION
      raise e

    if project.private_key != private:
      e = exceptions.AuthenticationFailed(detail='Invalid authentication credentials')
      e.errno = INVALID_PROJECT_AUTHENTICATION
      raise e

    # Hacky solution so django-rest-framework does not through exception
    project.is_authenticated = lambda : True
    
    project.last_api_activity = timezone.now()
    project.save()

    return (project, None)
