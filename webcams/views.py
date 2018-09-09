from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import Webcam

def index(request):
  return redirect("http://roboclubx.roboclub.org/public.html")
  # This is the original webcam code.
  webcams = Webcam.objects.all().filter()
  urls = [webcam.url for webcam in webcams]
  return render(request, 'webcams/index.jade', {'webcams': webcams, 'urls': urls})
  
