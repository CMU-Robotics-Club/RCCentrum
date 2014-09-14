from rest_framework import routers, serializers, viewsets
from .views import RoboUserViewSet, ProjectViewSet, OfficerViewSet

router = routers.DefaultRouter()
router.register(r'users', RoboUserViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'officers', OfficerViewSet)

urlpatterns = router.urls