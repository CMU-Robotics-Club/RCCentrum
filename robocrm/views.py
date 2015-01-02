from django.http import HttpResponse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from api.models import APIRequest
from django.views.decorators.http import require_POST
from projects.models import Project
from .models import *

def roboauth(request, rfid_tag, mach_num):
  r = RoboUser.objects.filter(rfid=rfid_tag)
  if r.count() > 0:
    us = r[0]
  else:
    return HttpResponse("0")
  auth_machines = us.machines.filter(id=mach_num)
  if auth_machines.count() > 0 :
    return HttpResponse("1")
  else :
    return HttpResponse("0")

def roboauthall(request, rfid_tag):
  r = RoboUser.objects.filter(rfid=rfid_tag)
  if r.count() > 0:
    us = r[0]
  else:
    return HttpResponse("0")
  auth = 0
  for mach in us.machines.all():
    auth |= 1 << int(mach.id)
  return HttpResponse(str(auth))

@require_POST
def add_card_event(request):
  if 'username' in request.POST and 'password' in request.POST:
    user = authenticate(username=request.POST['username'],
        password=request.POST['password'])
    if user is not None and user.is_active:
      login(request, user)

  if not request.user.is_authenticated() \
      or not request.user.has_perm('robocrm.add_event'):
    raise PermissionDenied

  tstart = request.POST['tstart'] # TODO: convert to date
  tend = request.POST['tend']
  user_id = request.POST['user_id']
  succ = request.POST['succ'] == '1'
  machine_id = int(request.POST['machine_id'])

  try:
    robouser = RoboUser.objects.get(rfid__iexact=user_id)
  except ObjectDoesNotExist:
    robouser = None

  machine = Machine.objects.get(id__exact=machine_id)

  api_request = APIRequest(
    endpoint="/rfid/",
    updater_object=Project.objects.get(name="Tooltron"),
    user=robouser,
    success=succ,
    meta=machine.type
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

  return HttpResponse()
