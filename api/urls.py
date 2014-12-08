from rest_framework import routers, serializers, viewsets
from .views import *
from django.conf.urls import include, patterns, url

router = routers.DefaultRouter()

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

router.register(r'magnetic', MagneticViewSet, base_name="magnetic")
router.register(r'rfid', RFIDViewSet, base_name="rfid")

#router.register(r'projects/datastore', MessageViewSet, base_name="datastore")

urlpatterns = router.urls
