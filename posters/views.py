from django.shortcuts import render, get_object_or_404
from .models import Poster

def index(request):
  posters = Poster.objects.all()
  return render(request, 'posters/index.jade', {'posters': posters})
