from rest_framework import routers, serializers, viewsets
from .views import *
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
router.register(r'sponsors', SponsorViewSet)
router.register(r'socialmedia', SocialMediaViewSet)

router.register(r'magnetic', MagneticViewSet, base_name="magnetic")
router.register(r'lookup/card', LookupCardViewSet, base_name="lookup_card")

#router.register(r'projects/message', MessageViewSet, base_name="message")
#router.register(r'projects/datastore', MessageViewSet, base_name="datastore")

urlpatterns = router.urls
