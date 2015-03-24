from django.http import HttpResponse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from api.models import APIRequest
from django.views.decorators.http import require_POST
from projects.models import Project
from django.utils import timezone
from .models import RoboUser, Machine
import dateutil.parser

def roboauth(request, rfid_tag, mach_num):
  machine = None

  try:
    machine = Machine.objects.get(toolbox_id__exact=mach_num)
    machine.rfid_present = True
    machine.save()
  except Machine.DoesNotExist:
    pass

  r = None

  try:
    r = RoboUser.objects.get(rfid=rfid_tag)
  except RoboUser.DoesNotExist:
    if machine:
      machine.user = None
      machine.save()

    return HttpResponse("0")

  if machine:
    machine.user = r
    machine.save()

  if not r.membership_valid:
    return HttpResponse("0")

  return HttpResponse(r.machines.filter(toolbox_id=mach_num).count())


@require_POST
def add_card_event(request):
  tstart = dateutil.parser.parse(request.POST.get('tstart'))
  user_id = request.POST.get('user_id')
  succ = request.POST.get('succ') == '1'
  machine_id = int(request.POST.get('machine_id'))

  try:
    robouser = RoboUser.objects.get(rfid__iexact=user_id)
  except ObjectDoesNotExist:
    robouser = None

  machine = Machine.objects.get(toolbox_id__exact=machine_id)

  machine.rfid_present = False
  machine.user = None
  machine.save()

  tooltron = Project.objects.get(name="Tooltron")

  api_request = APIRequest(
    endpoint="/rfid/",
    updater_object=tooltron,
    user=robouser,
    success=succ,
    meta=machine.type,
    api_client="",
  )

  api_request.save()

  # Cannot update updated_datetime with tend
  # because would be overwritten on save however
  # does not matter because Tooltron pushes
  # card events every 70ms which a lower resolution
  # that what tend even provides so update_datetime
  # being the value when this save() is called is okay 
  api_request.created_datetime = tstart
  api_request.save()

  # Since Tooltron (for now) does not use Standard API
  # manually update it's last_activity field so Officers have the benefit
  # of easily being able to see if it is working
  tooltron.last_api_activity = timezone.now()
  tooltron.save()

  return HttpResponse()
