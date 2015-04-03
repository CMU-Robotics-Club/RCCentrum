from rest_framework import status
from .authenticated_api_test_case import AuthenticatedAPITestCase

class CalendarTests(AuthenticatedAPITestCase):

  def test_success(self):
    """
    Ensure 200 Response Code
    """

    response = self.client.get("/api/calendar/", {}, **self.headers)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_query_param_dt_success(self):
    """
    Ensure 200 Response Code
    """

    response = self.client.get("/api/calendar/?dt=2015-04-03T18:10:28", {}, **self.headers)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
