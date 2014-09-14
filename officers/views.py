from django.shortcuts import render, get_object_or_404
from .models import Officer

def index(request):
  officers = Officer.objects.all()
  return render(request, 'officers/index.jade', {'officers': officers})

def detail(request, officer_id):
  officer = get_object_or_404(Officer, pk=officer_id)
  return render(request, 'officers/detail.jade', {'officer': officer})