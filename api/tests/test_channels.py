from rest_framework import status
from dateutil import parser
from .authenticated_api_test_case import AuthenticatedAPITestCase
from channels.models import Channel

class ChannelTests(AuthenticatedAPITestCase):

  def setUp(self):
    super().setUp()

    self.channel = Channel.objects.create(name="TestChannel", updater_object=self.project)

  def test_get_channel_anonymous(self):
    """
    Do not pass credentials in 'client.get' since Channels can be read
    anonymously.
    """

    response = self.client.get("/api/channels/{}/".format(self.channel.id), {}, {})
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    self.assertEqual(sorted(response.data.keys()), sorted(['id', 'name', 'created', 'updated', 'value', 'description']))
    self.assertEqual(response.data['id'], self.channel.id)
    self.assertEqual(response.data['name'], self.channel.name)
    self.assertEqual(parser.parse(response.data['created']), self.channel.created_datetime.replace(microsecond=0))
    self.assertEqual(parser.parse(response.data['updated']), self.channel.updated_datetime.replace(microsecond=0))
    self.assertEqual(response.data['value'], self.channel.value)
    self.assertEqual(response.data['description'], self.channel.description)


  def test_get_channel_fields(self):
    response = self.client.get("/api/channels/{}/?fields=id".format(self.channel.id), {}, {})
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    self.assertEqual(sorted(response.data.keys()), sorted(['id']))
    self.assertEqual(response.data['id'], self.channel.id)

  def test_get_channel_exclude(self):
    response = self.client.get("/api/channels/{}/?exclude=name,created,updated,value,description".format(self.channel.id), {}, {})
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    self.assertEqual(sorted(response.data.keys()), sorted(['id']))
    self.assertEqual(response.data['id'], self.channel.id)

  def test_put_channel_value_authenticated(self):
    response = self.client.put("/api/channels/{}/".format(self.channel.id), {'value': 'Hello'}, **self.headers)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(Channel.objects.get(id=self.channel.id).value, "Hello")

  def test_put_channel_value_anonymous(self):
    response = self.client.put("/api/channels/{}/".format(self.channel.id), {'value': 'Hello'}, {})
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    self.assertEqual(Channel.objects.get(id=self.channel.id).value, None)

  def test_put_channel_name(self):
    """
    Test that channel name is read-only via REST API.
    """

    original_name = self.channel.name

    response = self.client.put("/api/channels/{}/".format(self.channel.id), {"name": "NewName"}, **self.headers)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(Channel.objects.get(id=self.channel.id).name, original_name)
