from rest_framework import viewsets
from robocrm.models import RoboUser
from projects.models import Project
from officers.models import Officer
from .serializers import RoboUserSerializer, ProjectSerializer, OfficerSerializer

class RoboUserViewSet(viewsets.ReadOnlyModelViewSet):
  model = RoboUser
  serializer_class = RoboUserSerializer

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
  model = Project
  serializer_class = ProjectSerializer

class OfficerViewSet(viewsets.ReadOnlyModelViewSet):
  model = Officer
  serializer_class = OfficerSerializer
