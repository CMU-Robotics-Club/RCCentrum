from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.utils.text import slugify
from crm.label import Label

def create_project_label(project):
    label = Label()
    org_start, org_end = label.add_text("#000000", (0,0), "Roboto-Thin.ttf", 200, "Carnegie Mellon Robotics Club")
    rect_start, rect_end = label.add_rectangle("#aaaaaa", (org_end[0] + 20, 0), (20, org_end[1]))
    type_start, type_end = label.add_text("#000000", (rect_end[0] + 20, 0), "Roboto-Regular.ttf", 200, "Official Club Project")

    name_start, name_end = label.add_text("#0000AA", (type_end[0]/2, rect_end[1] + 80), "Roboto-Regular.ttf", 400, project.name, True)

    project_url = "{}{}".format(str(Site.objects.get_current()), reverse('projects:detail-name', args=(slugify(project.name),)))
    url_start, url_end = label.add_text("#000000", (type_end[0]/2, name_end[1] + 80), "Roboto-Thin.ttf", 200, project_url, True)
  
    return label.create()
