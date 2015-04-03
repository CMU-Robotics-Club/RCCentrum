from rest_framework import status
from .authenticated_api_test_case import AuthenticatedAPITestCase
from robocrm.models import Machine
from projects.models import Project

class MachineTests(AuthenticatedAPITestCase):

    def setUp(self):
        super().setUp()

        self.tooltron_machine = Machine.objects.create(id='1', type="Drill Press", toolbox_id=2)

        # Non-tooltron machine because no 'toolbox_id' is provided
        self.nontooltron_machine = Machine.objects.create(id='2', type="Lathe")

    def test_get_machines_anonymous(self):
        """
        Do not pass credentials in 'client.get' since Machines can be read
        anonymously.
        """

        response = self.client.get("/api/machines/", {}, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_machine_anonymous(self):
        """
        Do not pass credentials in 'client.get' since Machines can be read
        anonymously.
        """

        response = self.client.get("/api/machines/{}/".format(self.tooltron_machine.id), {}, {})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(sorted(response.data.keys()), sorted(['id', 'type', 'toolbox_id', 'rfid_present', 'user', 'powered']))
        self.assertEqual(response.data['id'], self.tooltron_machine.id)
        self.assertEqual(response.data['type'], self.tooltron_machine.type)
        self.assertEqual(response.data['rfid_present'], False)
        self.assertEqual(response.data['user'], None)
        self.assertEqual(response.data['powered'], False)

    def test_filter_machines_toolbox_id_is_null_false(self):
        """
        Needed by Tooltron to only get Machines that have Toolbox IDs.
        """

        response = self.client.get("/api/machines/?toolbox_id__isnull=False", {}, {})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(sorted(response.data[0].keys()), sorted(['id', 'type', 'toolbox_id', 'rfid_present', 'user', 'powered', ]))
        self.assertEqual(response.data[0]['id'], self.tooltron_machine.id)
        self.assertEqual(response.data[0]['type'], self.tooltron_machine.type)

    def test_machine_powered_forbidden(self):
        """
        Attempt to set machine 'powered' field but received 403
        because not authenticated as Tooltron project. 
        """
        
        project = Project.objects.create(name='Test')

        headers = {
          'HTTP_PUBLIC_KEY': project.id,
          'HTTP_PRIVATE_KEY': project.private_key
        }

        response = self.client.put("/api/machines/{}/".format(self.tooltron_machine.id), {'powered': True}, **headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_machine_powered_success(self):
        """
        Set machine 'powered' field.
        """

        project = Project.objects.create(name='Tooltron')

        headers = {
          'HTTP_PUBLIC_KEY': project.id,
          'HTTP_PRIVATE_KEY': project.private_key
        }

        response = self.client.put("/api/machines/{}/".format(self.tooltron_machine.id), {'powered': True}, **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(sorted(response.data.keys()), sorted(['id', 'type', 'toolbox_id', 'rfid_present', 'user', 'powered']))
        self.assertEqual(response.data['id'], self.tooltron_machine.id)
        self.assertEqual(response.data['type'], self.tooltron_machine.type)
        self.assertEqual(response.data['rfid_present'], False)
        self.assertEqual(response.data['user'], None)
        self.assertEqual(response.data['powered'], True)
