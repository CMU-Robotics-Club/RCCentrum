from django.test import TestCase
from django.contrib.auth.models import User
from robocrm.models import RoboUser, Machine
from projects.models import Project
from api.models import APIRequest
from django.test.client import Client
from rest_framework import status
from rest_framework.test import APITestCase
import dateutil.parser


class TooltronViewTests(APITestCase):

    def setUp(self):
      self.tooltron_project = Project.objects.create(name='Tooltron')

      self.user = User.objects.create(username="bstrysko", first_name="Brent", last_name="Strysko")
      self.robouser = RoboUser.objects.create(user=self.user, rfid="12345678")

      self.testTool = Machine.objects.create(id='1', type="TestTool", toolbox_id=1)
      self.robouser.machines.add(self.testTool)


    def test_roboauth_success(self):
      response = self.client.get("/crm/roboauth/{}/{}/".format(self.robouser.rfid, self.testTool.id), {})
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(response.content, b'1')

      self.testTool = Machine.objects.get(id=self.testTool.id)
      self.assertEqual(self.testTool.rfid_present, True)
      self.assertEqual(self.testTool.user, self.robouser)

    def test_roboauth_fail_rfid(self):
      response = self.client.get("/crm/roboauth/{}/{}/".format('1234567F', self.testTool.id), {})
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(response.content, b'0')

      self.testTool = Machine.objects.get(id=self.testTool.id)
      self.assertEqual(self.testTool.rfid_present, True)
      self.assertEqual(self.testTool.user, None)

    def test_roboauth_fail_membership_valid(self):
      self.robouser.dues_paid = "1990-01-01"
      self.robouser.save()
      
      response = self.client.get("/crm/roboauth/{}/{}/".format(self.robouser.rfid, self.testTool.id), {})
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(response.content, b'0')

      self.testTool = Machine.objects.get(id=self.testTool.id)
      self.assertEqual(self.testTool.rfid_present, True)
      self.assertEqual(self.testTool.user, self.robouser)

    def test_roboauth_fail_machine(self):
      response = self.client.get("/crm/roboauth/{}/{}/".format(self.robouser.rfid, '1000'), {})
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(response.content, b'0')

      self.testTool = Machine.objects.get(id=self.testTool.id)
      self.assertEqual(self.testTool.rfid_present, False)
      self.assertEqual(self.testTool.user, None)

    def test_add_card_event(self):
      response = self.client.post("/crm/add_card_event/", {
        'tstart': '1993-01-02 12:00:01',
        'user_id': self.robouser.rfid,
        'succ': '0',
        'machine_id': self.testTool.id
      })

      self.assertEqual(response.status_code, status.HTTP_200_OK)

      self.assertEqual(APIRequest.objects.all().count(), 1)

      apiRequest = APIRequest.objects.all()[0]

      self.assertEqual(apiRequest.endpoint, '/rfid/')
      self.assertEqual(apiRequest.updater_object, self.tooltron_project)
      self.assertEqual(apiRequest.user, self.robouser)
      self.assertEqual(apiRequest.success, False)
      self.assertEqual(apiRequest.meta, self.testTool.type)

      self.assertEqual(apiRequest.created_datetime, dateutil.parser.parse('1993-01-02 12:00:01'))

      self.testTool = Machine.objects.get(id=self.testTool.id)
      self.assertEqual(self.testTool.rfid_present, False)
      self.assertEqual(self.testTool.user, None)

    def test_success_scenario(self):
      """
      Combination of previous success tests.
      """

      self.assertEqual(self.testTool.rfid_present, False)
      self.assertEqual(self.testTool.user, None)

      response = self.client.get("/crm/roboauth/{}/{}/".format(self.robouser.rfid, self.testTool.id), {})
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(response.content, b'1')

      self.testTool = Machine.objects.get(id=self.testTool.id)
      self.assertEqual(self.testTool.rfid_present, True)
      self.assertEqual(self.testTool.user, self.robouser)

      response = self.client.post("/crm/add_card_event/", {
        'tstart': '1993-01-02 12:00:01',
        'user_id': self.robouser.rfid,
        'succ': '0',
        'machine_id': self.testTool.id
      })

      self.assertEqual(response.status_code, status.HTTP_200_OK)

      self.assertEqual(APIRequest.objects.all().count(), 1)

      apiRequest = APIRequest.objects.all()[0]

      self.assertEqual(apiRequest.endpoint, '/rfid/')
      self.assertEqual(apiRequest.updater_object, self.tooltron_project)
      self.assertEqual(apiRequest.user, self.robouser)
      self.assertEqual(apiRequest.success, False)
      self.assertEqual(apiRequest.meta, self.testTool.type)

      self.assertEqual(apiRequest.created_datetime, dateutil.parser.parse('1993-01-02 12:00:01'))

      self.testTool = Machine.objects.get(id=self.testTool.id)
      self.assertEqual(self.testTool.rfid_present, False)
      self.assertEqual(self.testTool.user, None)
