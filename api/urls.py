from rest_framework import routers, serializers, viewsets
from .views import LoginViewSet, WebcamViewSet, DateTimeViewSet, RoboUserViewSet, ProjectViewSet, OfficerViewSet, MessageViewSet, CalendarViewSet
from django.conf.urls import include, patterns, url

router = routers.DefaultRouter()

router.register(r'login', LoginViewSet, base_name="login")
router.register(r'webcam', WebcamViewSet)
router.register(r'datetime', DateTimeViewSet, base_name="datetime")
router.register(r'users', RoboUserViewSet)
router.register(r'officers', OfficerViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'messages', MessageViewSet, base_name="messages")
router.register(r'calendar', CalendarViewSet, base_name="calendar")

router.register(r'projects/active', MessageViewSet, base_name="active")
#router.register(r'projects/message', MessageViewSet, base_name="message")
#router.register(r'projects/datastore', MessageViewSet, base_name="datastore")

urlpatterns = router.urls
