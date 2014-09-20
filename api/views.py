from rest_framework import viewsets
from robocrm.models import RoboUser
from projects.models import Project
from officers.models import Officer
from webcams.models import Webcam
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
#from rest_framework.decorators import detail_route, list_route
from .serializers import WebcamSerializer, RoboUserSerializer, ProjectSerializer, OfficerSerializer
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.exceptions import ParseError, NotAuthenticated
from .errno import *

# TODO: figure out why import detail_route and list_route does not work
def detail_route(methods=['get'], **kwargs):
  def decorator(func):
    func.bind_to_methods = methods
    func.list = False
    func.detail = True
    func.kwargs = kwargs
    return func
  return decorator

def list_route(methods=['get'], **kwargs):
  def decorator(func):
    func.bind_to_methods = methods
    func.detail = False
    func.list = True
    func.kwargs = kwargs
    return func
  return decorator



class WebcamViewSet(viewsets.ReadOnlyModelViewSet):

  model = Webcam
  serializer_class = WebcamSerializer
  filter_fields = ('name', )

class DateTimeViewSet(viewsets.ViewSet):

  def list(self, request):
    return Response(timezone.now())


class RoboUserViewSet(viewsets.ReadOnlyModelViewSet):

  model = RoboUser
  serializer_class = RoboUserSerializer
  filter_fields = ('club_rank', )

  @list_route(methods=['post'])
  def login(self, request):
    data = JSONParser().parse(request)
    username = data.get('username', None)
    password = data.get('password', None)

    if username is None or password is None:
      # TODO: return something not 200
      error = ParseError(detail="Username and Password must be provided")
      error.errno = USERNAME_OR_PASSWORD_NONE
      raise error

    user = authenticate(username=username, password=password)

    valid = user is not None
    return Response(valid)

class OfficerViewSet(viewsets.ReadOnlyModelViewSet):

  model = Officer
  serializer_class = OfficerSerializer
  filter_fields = ('position', 'user', 'order', )


messages = {}
message_id = 0

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
  
  model = Project
  serializer_class = ProjectSerializer
  filter_fields = ('name', 'display', 'leaders', )

  @list_route()
  def active(self, request):
    time_threshold = timezone.now() - timedelta(minutes=5)
    active_projects = Project.objects.filter(last_api_activity__gte=time_threshold)

    active_project_ids = [project.id for project in active_projects]

    return Response(active_project_ids)

  @detail_route(methods=['get', 'post'])
  def messages(self, request, pk):
    pk = int(pk)

    if request.method == 'GET':
      message_response = []

      if pk in messages:
        message_response = messages[pk]

        # If project sees its own messages, clear them
        project = request._user

        if type(project).__name__ == 'Project' and project.id == pk:
          messages[pk] = []

      return Response(message_response)

    # Post
    else:
      project = request._user

      if type(project).__name__ != 'Project':
        error = NotAuthenticated(detail="Can only create messages as a project")
        error.errno = NOT_AUTHENTICATED_AS_PROJECT
        raise error
      elif project.id != pk:
        error = NotAuthenticated(detail="You are not this project")
        error.errno = NOT_AUTHENTICATED_AS_THIS_PROJECT
        raise error
      else:
        # Authenticated

        data = JSONParser().parse(request)

        to_project_id = data.get('to', None)
        message = data.get('message', None)

        if to_project_id is None or message is None:
          error = ParseError(detail="Invalid message")
          error.errno = INVALID_MESSAGE_STRUCTURE
          raise error

        try:
          to_project = Project.objects.get(id=to_project_id)
        except Project.DoesNotExist:
          error = ParseError(detail="Invalid to project ID")
          error.errno = INVALID_PROJECT_ID
          raise error

        global message_id
        m_id = message_id
        message_id += 1

        new_message = {
          "from": pk,
          "id": m_id,
          "message": message
        }

        if to_project_id in messages:
          messages[to_project_id].append(new_message)
        else:
          messages[to_project_id] = [new_message]

        return Response(m_id)

  @detail_route(methods=['get', 'post'])
  def datastore(self, request, pk):
    # TODO: implement
    pk = int(pk)

    return Response()
