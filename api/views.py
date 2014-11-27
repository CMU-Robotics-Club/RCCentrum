from rest_framework import viewsets
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
#from rest_framework.decorators import detail_route, list_route
from rest_framework.decorators import *
from .serializers import *
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.exceptions import APIException, ParseError, NotAuthenticated, AuthenticationFailed, PermissionDenied
from .errno import *
from .google_api import get_calendar_events
import dateutil.parser
from django.conf import settings
from django.utils import timezone
from .filters import RoboUserFilter, ChannelFilter
from rest_framework.viewsets import GenericViewSet
from tshirts.models import TShirt
from django.core.mail import send_mail
import logging
from posters.models import Poster
from .models import APIRequest
from rest_framework_extensions.cache.decorators import cache_response

logger = logging.getLogger(__name__)

# TODO: figure out why import detail_route and list_route does not work
def detail_route(methods=['get'], **kwargs):
  def decorator(func):
    func.bind_to_methods = methods
    func.list = False
    func.detail = True
    func.kwargs = kwargs
    return func
  return decorator

def list_route(methods=['get'], **kwargs):
  def decorator(func):
    func.bind_to_methods = methods
    func.detail = False
    func.list = True
    func.kwargs = kwargs
    return func
  return decorator

# TODO: clean this up by overriding method in a base class
# and having all views in this file extend that instead
# of the current fix of method patching

# Place api_request in self
# so View specific methods can override
old_initial = APIView.initial
def new_initial(self, request, *args, **kwargs):
  endpoint = request.path.replace("/api", "")
  user = request.user

  api_request = APIRequest(
    endpoint = endpoint,
    requester_object = user,
  )

  self.api_request = api_request

  return old_initial(self, request, *args, **kwargs)
APIView.initial = new_initial

old_finalize_response = APIView.finalize_response
def new_finalize_response(self, request, response, *args, **kwargs):
  self.api_request.save()
  return old_finalize_response(self, request, response, *args, **kwargs)
APIView.finalize_response = new_finalize_response


class LoginViewSet(viewsets.ViewSet):
  """
  Return True if the fields 'username' and 'password'
  in a POST request are valid user credentials.
  """

  # So details can easily be gotten through
  # browsing the API
  def list(self, request):
    error = ParseError(detail="Username and Password must be provided")
    error.errno = USERNAME_OR_PASSWORD_NONE
    raise error

  # Actual action
  def create(self, request):
    data = JSONParser().parse(request)
    username = data.get('username', None)
    password = data.get('password', None)

    if username is None or password is None:
      error = ParseError(detail="Username and Password must be provided")
      error.errno = USERNAME_OR_PASSWORD_NONE
      raise error

    user = authenticate(username=username, password=password)

    valid = user is not None

    if valid:
      if hasattr(user, 'robouser'):
        self.api_request.user = user.robouser
      else:
        self.api_request.meta = user

    return Response(valid)
    

class WebcamViewSet(viewsets.ReadOnlyModelViewSet):
  """
  The Club's Webcams.
  """

  model = Webcam
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

  model = RoboUser
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

        # TODO: return something other than just True
        return Response(True)

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

        from_address = "{}@roboticsclub.org".format(project.name)

        data = JSONParser().parse(request)
        subject = data.get('subject', None)
        body = data.get('body', None)

        send_mail(subject, body, from_address, [user.user.email])

        return Response(True)
      else:
        # Possibly make this case a unique errno
        error = PermissionDenied(detail="This project is not authenticated to perform this operation")
        error.errno = INSUFFICIENT_PROJECT_PERMISSIONS
        raise error

class OfficerViewSet(viewsets.ReadOnlyModelViewSet):
  """
  The officers of the Robotics Club.
  """

  model = Officer
  serializer_class = OfficerSerializer
  filter_fields = ('id', 'position', 'user', 'order', )


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
  """
  Club Projects
  """

  model = Project
  serializer_class = ProjectSerializer
  filter_fields = ('id', 'name', 'display', 'leaders', )


class ChannelViewSet(viewsets.ModelViewSet):

  model = Channel
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
  model = Sponsor
  serializer_class = SponsorSerializer
  filter_fields = ('id', 'name', 'active', )


class SocialMediaViewSet(viewsets.ReadOnlyModelViewSet):
  model = SocialMedia
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

    dt = self.request.QUERY_PARAMS.get('dt', None)

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

    card_id = request.DATA

    try:
      robouser = RoboUser.objects.get(magnetic=card_id)
      self.api_request.user = robouser
      return Response(robouser.id)
    except RoboUser.DoesNotExist:
      error = APIException(detail="Magnetic ID has no such member")
      error.errno = MAGNETIC_NO_MEMBER
      error.status_code = 400
      raise error

class RFIDViewSet(viewsets.ViewSet):
  """
  Returns the RoboUser ID associated with the specified CMU RFID tag.
  If no such user exists returns a HTTP Status code of 400.
  """

  def create(self, request):
    rfid = request.DATA

    logger.debug("RFID lookup {}".format(rfid))

    try:
      robouser = RoboUser.objects.get(rfid=rfid)
      self.api_request.user = robouser
      return Response(robouser.id)
    except RoboUser.DoesNotExist:
      error = APIException(detail="RFID has no such member")
      error.errno = RFID_NO_MEMBER
      error.status_code = 400
      raise error


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
  model = Category
  serializer_class = CategorySerializer
  filter_fields = ('id', 'title', )


class TShirtViewSet(viewsets.ReadOnlyModelViewSet):
  model = TShirt
  serializer_class = TShirtSerializer
  filter_fields = ('id', 'name', 'year', )


class PosterViewSet(viewsets.ReadOnlyModelViewSet):
  model = Poster
  serializer_class = PosterSerializer
  filter_fields = ('id', 'name', 'year', )


# TODO: move to machines app
from robocrm.models import Machine

class MachineViewSet(viewsets.ReadOnlyModelViewSet):
  model = Machine
  serializer_class = MachineSerializer
  filter_fields = ('id', 'type', )
