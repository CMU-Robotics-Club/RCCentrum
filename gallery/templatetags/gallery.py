from django import template
from ..models import Photo

register = template.Library()

@register.assignment_tag
def get_gallery():
  """
  Returns all Photos that should be displayed.
  """

  return Photo.objects.filter(display=True)
