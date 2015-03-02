from rest_framework import routers, serializers, viewsets
from .views import *
from django.conf.urls import include, patterns, url

router = routers.DefaultRouter()

router.register(r'api_requests', APIRequestViewSet)
router.register(r'webcams', WebcamViewSet)
router.register(r'datetime', DateTimeViewSet, base_name="datetime")
router.register(r'users', RoboUserViewSet)
router.register(r'officers', OfficerViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'channels', ChannelViewSet, base_name="channels")
router.register(r'calendar', CalendarViewSet, base_name="calendar")
router.register(r'sponsors', SponsorViewSet)
router.register(r'social_medias', SocialMediaViewSet)
router.register(r'machines', MachineViewSet)
router.register(r'faq', CategoryViewSet)
router.register(r'tshirts', TShirtViewSet)
router.register(r'posters', PosterViewSet)
router.register(r'upcs', UPCItemViewSet, base_name="upcs")


urlpatterns = router.urls + [
  url(r'^magnetic/$', MagneticView.as_view()),
  url(r'^rfid/$', RFIDView.as_view()),
]
