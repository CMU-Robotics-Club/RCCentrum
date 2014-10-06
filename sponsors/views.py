from django.shortcuts import render, get_object_or_404
from .models import Sponsor

def index(request):
  active_sponsors = Sponsor.objects.all().filter(active=True)
  inactive_sponsors = Sponsor.objects.all().filter(active=False)

  return render(request, 'sponsors/index.jade', {'active_sponsors': active_sponsors, 'inactive_sponsors': inactive_sponsors})
