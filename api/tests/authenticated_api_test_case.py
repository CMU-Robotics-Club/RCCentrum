from rest_framework.test import APITestCase
from projects.models import Project

class AuthenticatedAPITestCase(APITestCase):

  def setUp(self):
    super().setUp()

    self.project = Project(name="TestProject", private_key="secret")
    self.project.save()

    self.headers = {
      'HTTP_PUBLIC_KEY': self.project.id,
      'HTTP_PRIVATE_KEY': self.project.private_key
    }
