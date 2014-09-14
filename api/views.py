from rest_framework import viewsets
from robocrm.models import RoboUser
from .serializers import RoboUserSerializer

class RoboUserViewSet(viewsets.ReadOnlyModelViewSet):
    model = RoboUser
    serializer_class = RoboUserSerializer
