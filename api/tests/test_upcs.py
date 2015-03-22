from rest_framework import status
from .authenticated_api_test_case import AuthenticatedAPITestCase
from upcs.format_upc import format_upc
from upcs.remote_lookup import remote_lookup

class UPCTests(AuthenticatedAPITestCase):

  def run_upc_test(self, upc):
    response = self.client.get("/api/upcs/?upc={}".format(upc), {}, **self.headers)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    if remote_lookup(format_upc(upc)) is not None:
      self.assertEqual(len(response.data), 1)

      self.assertEqual(sorted(response.data[0].keys()), sorted(['id', 'name', 'upc', 'cost']))
      self.assertEqual(response.data[0]['name'], remote_lookup(format_upc(upc)))
      self.assertEqual(response.data[0]['upc'], format_upc(upc))
    else:
      self.assertEqual(len(response.data), 0)


  def test_get_upce_8(self):
    self.run_upc_test("04043506")

  def test_get_upce_7(self):
    self.run_upc_test("0404350")

  def test_get_upce_6(self):
    self.run_upc_test("404350")

  def test_get_upca(self):
    self.run_upc_test("044000037420")

  def test_get_invalid(self):
    self.run_upc_test("04400007420")