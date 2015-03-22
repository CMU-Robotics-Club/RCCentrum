from rest_framework import status
from .authenticated_api_test_case import AuthenticatedAPITestCase

class UserTests(AuthenticatedAPITestCase):

  def test_get_users_authenticated(self):
    response = self.client.get("/api/users/", {}, **self.headers)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_get_users_anonymous(self):
    response = self.client.get("/api/users/", {}, {})
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)