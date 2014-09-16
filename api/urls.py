from rest_framework import routers, serializers, viewsets
from .views import datetime_view, DateTimeViewSet, RoboUserViewSet, ProjectViewSet, OfficerViewSet
from django.conf.urls import include, patterns, url

router = routers.DefaultRouter()

router.register(r'datetime', DateTimeViewSet, base_name="datetime")
router.register(r'users', RoboUserViewSet)
router.register(r'officers', OfficerViewSet)
router.register(r'projects', ProjectViewSet)

urlpatterns = router.urls
