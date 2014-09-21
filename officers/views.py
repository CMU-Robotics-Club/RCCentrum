from django.shortcuts import render, get_object_or_404
from .models import Officer

def index(request):
  officers = Officer.objects.all()
  return render(request, 'officers/index.jade', {'officers': officers})

def detail_id(request, officer_id):
  officer = get_object_or_404(Officer, pk=officer_id)
  return render(request, 'officers/detail.jade', {'officer': officer})

def detail_name(request, officer_username):
  officer = get_object_or_404(Officer, user__user__username=officer_username)
  return render(request, 'officers/detail.jade', {'officer': officer})
