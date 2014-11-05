from django.shortcuts import render, get_object_or_404
from .models import TShirt

def index(request):
  tshirts = TShirt.objects.all()
  return render(request, 'tshirts/index.jade', {'tshirts': tshirts})
