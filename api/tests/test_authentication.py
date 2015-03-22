from rest_framework.test import APITestCase
from projects.models import Project
from rest_framework import status

class AuthenticationTests(APITestCase):

  def test_forbidden(self):
    response = self.client.get("/api/")
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

  def test_success(self):
    project = Project(name="TestProject", private_key="secret")
    project.save()

    headers = {
      'HTTP_PUBLIC_KEY': project.id,
      'HTTP_PRIVATE_KEY': project.private_key
    }

    response = self.client.get("/api/", {}, **headers)
    self.assertEqual(response.status_code, status.HTTP_200_OK)