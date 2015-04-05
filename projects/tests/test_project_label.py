from django.test import TestCase
from projects.models import Project
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from robocrm.models import RoboUser

class ProjectLabelTests(TestCase):
  
  def setUp(self):
    self.project = Project.objects.create(name='TestProject')

  def test_get_label_id(self):
    """
    Get label from public website via project ID.
    """

    response = self.client.get(reverse('projects:label-id', args=(self.project.id, )))
    self.assertEqual(response.status_code, 200)

  def test_get_label_name(self):
    """
    Get label from public website via project name.
    """

    response = self.client.get(reverse('projects:label-name', args=(self.project.name, )))
    self.assertEqual(response.status_code, 200)

  def test_get_label_superuser_admin(self):
    """
    Should also be able to get label through admin interface.
    """
    
    password = 'test'
    user = User.objects.create_superuser(username="bstrysko", email="test@gmail.com", password=password)
    robouser = RoboUser.objects.create(user=user)

    self.assertTrue(self.client.login(username=user.username, password=password))

    response = self.client.get("/admin/projects/project/{}/tools/create_project_label/".format(self.project.id))
    self.assertEqual(response.status_code, 200)
