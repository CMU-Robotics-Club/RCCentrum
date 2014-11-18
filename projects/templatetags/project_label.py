from django.conf import settings
from django.template import Library

from projects.label import load_label

register = Library()

@register.filter
def project_label(project):
    '''
    Usage:
    {{project|project_label|safe}}
    '''

    label_filename, label_path = load_label(project) 
    
    label_url = "{}{}/{}".format(settings.MEDIA_URL, "project_labels", label_filename)
    link = '<a href="{}" target="_blank" >Project Label</a>'.format(label_url)
    return link
