from django.shortcuts import render, get_object_or_404
from .models import Webcam

def index(request):
  webcams = Webcam.objects.all().filter()
  urls = [webcam.url for webcam in webcams]
  return render(request, 'webcams/index.jade', {'webcams': webcams, 'urls': urls})