from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from robocrm.models import RoboUser
from projects.models import Project
from officers.models import Officer
from webcams.models import Webcam
from social_media.models import SocialMedia
from sponsors.models import Sponsor
from faq.models import Category, QA
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
from .filters import APIRequestFilter, RoboUserFilter, ChannelFilter
from rest_framework.viewsets import GenericViewSet
from tshirts.models import TShirt
from django.core.mail import send_mail
import logging
from posters.models import Poster
from .models import APIRequest
from rest_framework_extensions.cache.decorators import cache_response
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from .permissions import IsAPIRequesterOrReadOnly

logger = logging.getLogger(__name__)


# TODO: clean this up by overriding method in a base class
# and having all views in this file extend that instead
# of the current fix of method patching
#
# Place api_request in self
# so View specific methods can override
old_initial = APIView.initial
def new_initial(self, request, *args, **kwargs):
  endpoint = request.path.replace("/api", "")
  user = request.user

  api_request = APIRequest(
    endpoint = endpoint,
    updater_object = user,
  )

  if isinstance(request.data, dict):
    api_request.meta = request.data.get('meta', "")
  else:
    error = ParseError(detail="Received data not in dictionary format")
    error.erno = NOT_DICT
    raise error

  self.api_request = api_request

  return old_initial(self, request, *args, **kwargs)
APIView.initial = new_initial


# APIRequest is a ModelViewSet without create and destroy abilities
class APIRequestViewSet(
                      #mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      #mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
  """
  A APIRequest is created whenever a sucessfully authenticated request
  is made to '/rfid/', '/magnetic/', '/users/id/rfid/', '/users/id/email/',
  or '/users/id/balance/'.
  """

  permission_classes = (IsAPIRequesterOrReadOnly, )

  # Only display API Requests by Projects since ones by Users
  # are just for testing and by only listing Project API Requests
  # do not need to expose ContentType endpoint, extra ContentType 
  # field, etc.
  queryset = APIRequest.objects.filter(updater_type=ContentType.objects.get_for_model(Project))
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
  Has '/rfid' and '/email' endpoints.
  """

  queryset = RoboUser.objects.all()
  serializer_class = RoboUserSerializer
  filter_class = RoboUserFilter

  # TODO: make UPDATE
  @detail_route(methods=['POST'])
  def rfid(self, request, pk):
    user = request._user

    if type(user).__name__ != 'Project':
      error = PermissionDenied(detail="Not authenticated as a project")
      error.errno = NOT_AUTHENTICATED_AS_PROJECT
      raise error
    elif user.id not in settings.RFID_POST_PROJECT_IDS:
      error = PermissionDenied(detail="This project is not authenticated to perform this operation")
      error.errno = INSUFFICIENT_PROJECT_PERMISSIONS
      raise error
    else:
      u = RoboUser.objects.filter(pk=pk)[0]

      rfid = request.DATA

      if not rfid:
        error = ParseError(detail="Empty RFID #")
        error.errno = EMPTY_POST
        raise error
      else:
        u.rfid = rfid
        u.save()

        self.api_request.user = u
        self.api_request.save()

        return Response({
          "updated": True,
          "api_request": self.api_request.id
        })

  @detail_route(methods=['POST'])
  def email(self, request, pk):
    project = request._user

    if type(project).__name__ != 'Project':
      error = PermissionDenied(detail="Not authenticated as a project")
      error.errno = NOT_AUTHENTICATED_AS_PROJECT
      raise error
    elif project.id not in settings.EMAIL_POST_PROJECT_IDS:
      error = PermissionDenied(detail="This project is not authenticated to perform this operation")
      error.errno = INSUFFICIENT_PROJECT_PERMISSIONS
      raise error
    else:

      # Check if project can send to this user
      user = RoboUser.objects.filter(pk=pk)[0]

      allowed_users = settings.EMAIL_POST_PROJECT_IDS[project.id]

      if allowed_users is None or user.id in allowed_users:

        from_address = "{}@roboticsclub.org".format(slugify(project.name))

        data = request.data
        subject = data.get('subject', '')
        body = data.get('body', '')

        send_mail(subject, body, from_address, [user.user.email])

        self.api_request.user = user
        self.api_request.save()

        return Response({
          "sent": True,
          "api_request": self.api_request.id
        })
      else:
        error = PermissionDenied(detail="This project is not authenticated to perform this operation")
        error.errno = INSUFFICIENT_PROJECT_PERMISSIONS
        raise error


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


class ChannelViewSet(viewsets.ModelViewSet):

  queryset = Channel.objects.all()
  serializer_class = ChannelSerializer
  filter_class = ChannelFilter

  # Called when POST to /channels/
  def create(self, request, *args, **kwargs):
    logger.debug("Channel create")

    response = super().create(request, *args, **kwargs)

    # TODO: make this better by changing
    # default exception to include errno
    if response.status_code != 201:
      error = ParseError(detail="Duplicate")
      error.errno = DUPLICATE
      raise error
    else:
      return response


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

class MagneticViewSet(viewsets.ViewSet):
  """
  Returns the RoboUser ID associated with the specified CMU Card ID.
  If no such user exists returns a HTTP status code of 400.
  """

  def create(self, request):
    """
    Returns the RoboUser ID associated with the Card ID sent in the POST body.
    """

    data = request.data
    magnetic = data.get('magnetic')
    # Cast to string so if a request
    # passes an integer .get does not
    # throw Multiple Users error
    magnetic = str(magnetic)

    logger.debug("Magnetic lookup {}".format(magnetic))

    try:
      robouser = RoboUser.objects.get(magnetic=magnetic)
      self.api_request.user = robouser
      self.api_request.save()
      return Response({
        "user": robouser.id,
        "api_request": self.api_request.id
      })
    except RoboUser.DoesNotExist:
      error = APIException(detail="Magnetic ID has no such member")
      error.errno = MAGNETIC_NO_MEMBER
      error.status_code = 400
      self.api_request.save()
      raise error


class RFIDViewSet(viewsets.ViewSet):
  """
  Returns the RoboUser ID associated with the specified CMU RFID tag.
  If no such user exists returns a HTTP Status code of 400.
  Request should contain a dictionary with keys 'rfid'(required)
  and 'meta'(optional).
  """

  def create(self, request):
    data = request.data

    rfid = data.get('rfid')
    # Cast to string so if a request
    # passes an integer .get does not
    # throw Multiple Users error
    rfid = str(rfid)

    logger.debug("RFID lookup {}".format(rfid))

    try:
      robouser = RoboUser.objects.get(rfid=rfid)
      self.api_request.user = robouser
      self.api_request.save()
      return Response({
        "user": robouser.id,
        "api_request": self.api_request.id
      })
    except RoboUser.DoesNotExist:
      error = APIException(detail="RFID has no such member")
      error.errno = RFID_NO_MEMBER
      error.status_code = 400
      self.api_request.save()
      raise error


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


# TODO: move to machines app
from robocrm.models import Machine

class MachineViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Machine.objects.all()
  serializer_class = MachineSerializer
  filter_fields = ('id', 'type', )
