from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from robocrm.models import RoboUser
from projects.models import Project
from officers.models import Officer
from webcams.models import Webcam
from social_media.models import SocialMedia
from sponsors.models import Sponsor
from faq.models import Category, QA
from robocrm.models import Machine
from rest_framework.response import Response
from channels.models import Channel
from rest_framework.parsers import JSONParser
from rest_framework.decorators import detail_route
from rest_framework.decorators import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException, ParseError, NotAuthenticated, AuthenticationFailed, PermissionDenied
from .errno import *
from .google_api import get_calendar_events
import dateutil.parser
from django.conf import settings
from django.utils import timezone
from .filters import *
from rest_framework.viewsets import GenericViewSet
from tshirts.models import TShirt
from django.core.mail import send_mail
import logging
from posters.models import Poster
from .models import APIRequest
from rest_framework_extensions.cache.decorators import cache_response
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from .permissions import IsAPIRequesterOrReadOnlyPermission, UserBalancePermission, UserRFIDPermission, UserEmailPermission
from django.db import IntegrityError
from rest_framework.generics import GenericAPIView, CreateAPIView
from django.shortcuts import redirect
from rest_framework import status

logger = logging.getLogger(__name__)


def create_api_request(request, serializer):
  """
  Helper function to construct
  an APIRequest and populate it's fields
  that are constructed from the request
  object and serializer 'meta' field.
  """

  # Fix so updater_id maps correctly since
  # API exposes RoboUser IDs not User IDs
  user = request.user

  if hasattr(user, 'robouser'):
    user = user.robouser

  return APIRequest(
    endpoint = request.path.replace("/api", ""),
    updater_object = user,
    meta = serializer.validated_data.get('meta', ""),
    api_client = request.META.get('HTTP_API_CLIENT', "")
  )


# APIRequestViewSet is a ModelViewSet without create and destroy abilities
class APIRequestViewSet(
                      #mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      #mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
  """
  A APIRequest is created whenever a sucessfully authenticated POST request
  is made to '/rfid/', '/magnetic/', '/users/:id/rfid/', '/users/:id/email/',
  or '/users/:id/balance/'.
  Users can successfully make POST requests to '/rfid/' and '/magnetic/' through
  the HTML API viewer however those requests are not shown here(only those made
  by projects are shown here).
  """

  permission_classes = (IsAPIRequesterOrReadOnlyPermission, )

  queryset = APIRequest.objects.all()
  serializer_class = APIRequestSerializer
  filter_class = APIRequestFilter


class WebcamViewSet(viewsets.ReadOnlyModelViewSet):
  """
  The Club's Webcams.
  """

  queryset = Webcam.objects.all()
  serializer_class = WebcamSerializer
  filter_fields = ('id', 'name', )


class DateTimeViewSet(viewsets.ViewSet):
  """
  The current datetime.  Exists so that projects
  without a realtime clock can easily get the datetime.
  """

  def list(self, request):
    return Response(timezone.now())


class RoboUserViewSet(viewsets.ReadOnlyModelViewSet):
  """
  The members of the Robotics Club.
  """

  queryset = RoboUser.objects.all()
  serializer_class = RoboUserSerializer
  filter_class = RoboUserFilter

  # rfid, email, and balance are special cases
  def get_serializer_class(self):
    path = self.request.path
    tokens = path.rsplit('/')
    tokens[:] = (x for x in tokens if x != "")

    if len(tokens):
      action = tokens[-1]
    
      if action == 'email':
        return EmailSerializer
      elif action == 'rfid':
        return RFIDSerializer
      elif action == 'balance':
        return BalanceSerializer
  
    return super().get_serializer_class()

  @detail_route(methods=['POST'], permission_classes=[UserBalancePermission, ])
  def balance(self, request, pk):
    """
    Increments/decrements a User's balance(privileged operation).
    ---

    serializer: api.serializers.BalanceSerializer
    """

    u = self.get_object()
    user = request._user

    serializer = BalanceSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    amount = serializer.validated_data['amount']

    u.balance += amount
    u.save()

    api_request = create_api_request(request, serializer)
    api_request.user = u
    api_request.extra = str(balance)
    api_request.save()

    return Response({
      "api_request": api_request.id
    })

  @detail_route(methods=['POST'], permission_classes=[UserRFIDPermission, ])
  def rfid(self, request, pk):
    """
    Set a Users RFID(privileged operation).
    ---

    serializer: api.serializers.RFIDSerializer
    """
    u = self.get_object()

    user = request._user

    serializer = RFIDSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    rfid = serializer.validated_data['rfid']

    u.rfid = rfid

    # save() causes server error
    try:
      u.save()
    except IntegrityError:
      error = ParseError(detail="RFID already belongs to another member.")
      error.errno = DUPLICATE
      raise error

    api_request = create_api_request(request, serializer)
    api_request.user = u
    api_request.save()

    return Response({
      "api_request": api_request.id
    })

  @detail_route(methods=['POST'], permission_classes=[UserEmailPermission, ])
  def email(self, request, pk):
    """
    Sends a User an email(privileged operation).
    ---

    serializer: api.serializers.EmailSerializer
    """

    user = self.get_object()
    project = request._user

    from_address = "{}@roboticsclub.org".format(slugify(str(project)))

    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    subject = serializer.validated_data['subject']
    content = serializer.validated_data['content']

    send_mail(subject, content, from_address, [user.user.email])

    api_request = create_api_request(request, serializer)
    api_request.extra = "Subject: {}, Body: {}".format(subject, content)
    api_request.user = user
    api_request.save()

    return Response({
      "api_request": api_request.id
    })


class OfficerViewSet(viewsets.ReadOnlyModelViewSet):
  """
  The officers of the Robotics Club.
  """

  queryset = Officer.objects.all()
  serializer_class = OfficerSerializer
  filter_fields = ('id', 'position', 'user', 'order', )


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
  """
  Club Projects
  """

  queryset = Project.objects.all()
  serializer_class = ProjectSerializer
  filter_fields = ('id', 'name', 'display', 'leaders', )


# ChannelViewSet is a ModelViewSet without create and destroy abilities
class ChannelViewSet(
                    #mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    #mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):

  queryset = Channel.objects.all()
  serializer_class = ChannelSerializer
  filter_class = ChannelFilter


class SponsorViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Sponsor.objects.all()
  serializer_class = SponsorSerializer
  filter_fields = ('id', 'name', 'active', )


class SocialMediaViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = SocialMedia.objects.all()
  serializer_class = SocialMediaSerializer
  filter_fields = ('id', 'name', )


class CalendarViewSet(viewsets.ViewSet):
  """
  Returns a list of events currently occuring on the club's calendar.
  Each event has the field 'name', 'location', 'start_time', and 'end_time'.
  The 'current time' can be changed by setting the URL parameter 'dt' to a specified datetime.
  """

  # TODO: key this to take into account dt
  #@cache_response(30)
  def list(self, request):
    """
    List the calendar events.
    """

    dt = self.request.query_params.get('dt', None)

    if not dt:
      # If no datetime specified use now
      dt = timezone.now()
    else:
      dt = dateutil.parser.parse(dt)

    events = get_calendar_events(dt)
    return Response(events)


class MagneticView(GenericAPIView):
  """
  Returns the RoboUser ID associated with the specified CMU Card ID
  and the APIRequest ID.
  """

  serializer_class = MagneticSerializer

  def post(self, request, *args, **kwargs):
    serializer = MagneticSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    magnetic = serializer.validated_data['magnetic']

    logger.info("Magnetic lookup {}".format(magnetic))

    api_request = create_api_request(request, serializer)      

    try:
      robouser = RoboUser.objects.get(magnetic=magnetic)

      api_request.user = robouser
      api_request.save()
      
      return Response({
        "found": True,
        "user": robouser.id,
        "api_request": api_request.id
      })
    except RoboUser.DoesNotExist:
      api_request.save()

      return Response({
        "found": False,
        "user": None,
        "api_request": api_request.id
      })


class RFIDView(GenericAPIView):
  """
  Returns the RoboUser ID associated with the specified CMU RFID tag
  and the APIRequest ID.
  """

  serializer_class = RFIDSerializer

  def post(self, request, *args, **kwargs):
    serializer = RFIDSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    rfid = serializer.validated_data['rfid']

    logger.info("RFID lookup {}".format(rfid))

    api_request = create_api_request(request, serializer)

    try:
      robouser = RoboUser.objects.get(rfid=rfid)
      
      api_request.user = robouser
      api_request.save()
      
      return Response({
        "found": True,
        "user": robouser.id,
        "api_request": api_request.id
      })
    except RoboUser.DoesNotExist:
      api_request.save()

      return Response({
        "found": False,
        "user": None,
        "api_request": api_request.id
      })


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  filter_fields = ('id', 'title', )


class TShirtViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = TShirt.objects.all()
  serializer_class = TShirtSerializer
  filter_fields = ('id', 'name', 'year', )


class PosterViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Poster.objects.all()
  serializer_class = PosterSerializer
  filter_fields = ('id', 'name', 'year', )


class MachineViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Machine.objects.all()
  serializer_class = MachineSerializer
  filter_fields = ('id', 'type', )


def login_redirect_docs(request):
  return redirect('/admin/login/?next=/docs/')
