from django.shortcuts import render, get_object_or_404
from .models import Project
import logging

logger = logging.getLogger(__name__)

def index(request):
  logger.debug("View project index")

  projects = Project.objects.all().filter(display=True)
  return render(request, 'projects/index.jade', {'projects': projects})

def detail_id(request, project_id):
  logger.debug("View project detail_id".format(project_id))

  project = get_object_or_404(Project, pk=project_id)
  return render(request, 'projects/detail.jade', {'project': project})

def detail_name(request, project_name):
  logger.debug("View project detail_name {}".format(project_name))

  project_name = project_name.replace('-', ' ')
  project = get_object_or_404(Project, name=project_name)
  return render(request, 'projects/detail.jade', {'project': project})
