from rest_framework import viewsets
from robocrm.models import RoboUser
from projects.models import Project
from officers.models import Officer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
#from rest_framework.decorators import detail_route, list_route
from .serializers import RoboUserSerializer, ProjectSerializer, OfficerSerializer
from django.utils import timezone
from datetime import timedelta

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

class RoboUserViewSet(viewsets.ReadOnlyModelViewSet):
  model = RoboUser
  serializer_class = RoboUserSerializer

class OfficerViewSet(viewsets.ReadOnlyModelViewSet):
  model = Officer
  serializer_class = OfficerSerializer


messages = {}

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
  model = Project
  serializer_class = ProjectSerializer

  @list_route()
  def active(self, request):
    time_threshold = timezone.now() - timedelta(minutes=5)
    active_projects = Project.objects.filter(last_api_activity__gte=time_threshold)

    active_project_ids = [project.id for project in active_projects]

    return Response({
      "project_ids": active_project_ids
    })

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

      return Response({
        "messages": message_response
      })

    # Post
    else:
      project = request._user

      if type(project).__name__ != 'Project':
        return Response({
          "status": "error",
          "detail": "Can only create messages as a project"
        })
      elif project.id != pk:
        return Response({
          "status": "error",
          "detail": "You are not this project"
        })
      else:
        # Authenticated

        data = JSONParser().parse(request)

        to_project_id = data.get('to_project_id', None)
        message = data.get('message', None)

        if to_project_id is None or message is None:
          return Response({
            "status": "error",
            "detail": "Invalid message"
          })

        try:
          to_project = Project.objects.get(id=to_project_id)
        except Project.DoesNotExist:
          return Response({
            "status": "error",
            "detail": "Invalid to Project ID"
          })

        new_message = {
          "from": pk,
          "message": message
        }

        if to_project_id in messages:
          messages[to_project_id].append(new_message)
        else:
          messages[to_project_id] = [new_message]

        print(messages)

        return Response({
          "status": "sent"
        })
