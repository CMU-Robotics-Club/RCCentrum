from django.template import Library
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.utils.text import slugify
from projects.label import create_project_label

register = Library()

@register.filter
def project_label(project):
    '''
    Usage:
    {{project|project_label|safe}}
    '''
    
    label_url = "{}{}".format(str(Site.objects.get_current()), reverse('projects:label-name', args=(slugify(project.name),)))
    link = '<a href="{}" target="_blank" >Project Label</a>'.format(label_url)
    return link
