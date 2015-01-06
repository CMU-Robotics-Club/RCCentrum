from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from projects.models import Project

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


class AuthenticatedAPITestCase(APITestCase):

  def setUp(self):
    super().setUp()

    self.project = Project(name="TestProject", private_key="secret")
    self.project.save()

    self.headers = {
      'HTTP_PUBLIC_KEY': self.project.id,
      'HTTP_PRIVATE_KEY': self.project.private_key
    }


class UserTests(AuthenticatedAPITestCase):

  def test_get_users(self):
    response = self.client.get("/api/users/", {}, **self.headers)
    self.assertEqual(response.status_code, status.HTTP_200_OK)


#class ChannelTests(AuthenticatedAPITestCase):
#  pass

#class PrivelegedTests(AuthenticatedAPITestCase):
#  pass
