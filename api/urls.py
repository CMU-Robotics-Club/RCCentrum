from rest_framework import routers, serializers, viewsets
from .views import RoboUserViewSet

router = routers.DefaultRouter()
router.register(r'users', RoboUserViewSet)

urlpatterns = router.urls