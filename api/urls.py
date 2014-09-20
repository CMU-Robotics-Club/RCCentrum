from rest_framework import routers, serializers, viewsets
from .views import LoginViewSet, WebcamViewSet, DateTimeViewSet, RoboUserViewSet, ProjectViewSet, OfficerViewSet
from django.conf.urls import include, patterns, url

router = routers.DefaultRouter()

router.register(r'login', LoginViewSet, base_name="login")
router.register(r'webcam', WebcamViewSet)
router.register(r'datetime', DateTimeViewSet, base_name="datetime")
router.register(r'users', RoboUserViewSet)
router.register(r'officers', OfficerViewSet)
router.register(r'projects', ProjectViewSet)

urlpatterns = router.urls
