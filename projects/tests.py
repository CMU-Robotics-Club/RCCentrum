from django.test import TestCase
from .models import Project
from django.core.urlresolvers import reverse

class ProjectLabelTests(TestCase):
  
  def test_get_label_name(self):
    project = Project(name="TestProject")
    project.save()

    response = self.client.get(reverse('projects:label-name', args=(project.name, )))
    self.assertEqual(response.status_code, 200)

  def test_get_label_id(self):
    project = Project(name="TestProject")
    project.save()

    response = self.client.get(reverse('projects:label-id', args=(project.id, )))
    self.assertEqual(response.status_code, 200)
