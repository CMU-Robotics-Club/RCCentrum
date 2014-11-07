from django.shortcuts import render
from .models import Category

def index(request):
  categories = Category.objects.all()
  return render(request, 'faq/index.jade', {'categories': categories})
