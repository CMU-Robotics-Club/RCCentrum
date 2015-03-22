from rest_framework import status
from django.contrib.auth.models import User
from api.models import APIRequest
from robocrm.models import RoboUser
from .authenticated_api_test_case import AuthenticatedAPITestCase

class LookupTests(AuthenticatedAPITestCase):
  """
  Test Magnetic and RFID lookup endpoints.
  """

  def setUp(self):
    super().setUp()

    self.user = User.objects.create(username="bstrysko", first_name="Brent", last_name="Strysko")
    self.robouser = RoboUser.objects.create(user=self.user, magnetic="123456789", rfid="12345678")

  def test_magnetic_found(self):
    response = self.client.post("/api/magnetic/", {
      "magnetic": self.robouser.magnetic,
      "meta": "Test"
    }, **self.headers)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['found'], True)
    self.assertEqual(response.data['user'], self.robouser.id)
    self.assertEqual(type(response.data['api_request']), int)

    api_request = APIRequest.objects.get(id=response.data['api_request'])

    self.assertEqual(api_request.meta, "Test")

  def test_magnetic_not_found(self):
    response = self.client.post("/api/magnetic/", {
      "magnetic": "111111111",
      "meta": "Test"
    }, **self.headers)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['found'], False)
    self.assertEqual(response.data['user'], None)
    self.assertEqual(type(response.data['api_request']), int)

    api_request = APIRequest.objects.get(id=response.data['api_request'])

    self.assertEqual(api_request.meta, "Test")

  def test_magnetic_invalid(self):
    response = self.client.post("/api/magnetic/", {
      "magnetic": "1",
      "meta": "Test"
    }, **self.headers)

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual('magnetic' in response.data.keys(), True)

    # No APIRequest created
    self.assertEqual(APIRequest.objects.all().count(), 0)

  def test_rfid_found(self):
    response = self.client.post("/api/rfid/", {
      "rfid": self.robouser.rfid,
      "meta": "Test"
    }, **self.headers)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['found'], True)
    self.assertEqual(response.data['user'], self.robouser.id)
    self.assertEqual(type(response.data['api_request']), int)

    api_request = APIRequest.objects.get(id=response.data['api_request'])

    self.assertEqual(api_request.meta, "Test")

  def test_rfid_not_found(self):
    response = self.client.post("/api/rfid/", {
      "rfid": "11111111",
      "meta": "Test"
    }, **self.headers)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['found'], False)
    self.assertEqual(response.data['user'], None)
    self.assertEqual(type(response.data['api_request']), int)

    api_request = APIRequest.objects.get(id=response.data['api_request'])

    self.assertEqual(api_request.meta, "Test")

  def test_rfid_invalid(self):
    response = self.client.post("/api/rfid/", {
      "rfid": "1",
      "meta": "Test"
    }, **self.headers)

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual('rfid' in response.data.keys(), True)

    # No APIRequest created
    self.assertEqual(APIRequest.objects.all().count(), 0)
