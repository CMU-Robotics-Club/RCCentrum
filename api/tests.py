from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from projects.models import Project
from channels.models import Channel
from dateutil import parser

from upcs.format_upc import format_upc
from upcs.remote_lookup import remote_lookup

import json

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


class ChannelTests(AuthenticatedAPITestCase):

  def setUp(self):
    super().setUp()

    self.channel = Channel(name="TestChannel", updater_object=self.project)
    self.channel.save()

  def test_get_channel(self):
    response = self.client.get("/api/channels/{}/".format(self.channel.id), {}, **self.headers)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    self.assertEqual(sorted(response.data.keys()), sorted(['id', 'name', 'created', 'updated', 'value', 'description']))
    self.assertEqual(response.data['id'], self.channel.id)
    self.assertEqual(response.data['name'], self.channel.name)
    self.assertEqual(parser.parse(response.data['created']), self.channel.created_datetime.replace(microsecond=0))
    self.assertEqual(parser.parse(response.data['updated']), self.channel.updated_datetime.replace(microsecond=0))
    self.assertEqual(response.data['value'], self.channel.value)
    self.assertEqual(response.data['description'], self.channel.description)


  def test_get_channel_fields(self):
    response = self.client.get("/api/channels/{}/?fields=id".format(self.channel.id), {}, **self.headers)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    self.assertEqual(sorted(response.data.keys()), sorted(['id']))
    self.assertEqual(response.data['id'], self.channel.id)

  def test_get_channel_exclude(self):
    response = self.client.get("/api/channels/{}/?exclude=name,created,updated,value,description".format(self.channel.id), {}, **self.headers)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    self.assertEqual(sorted(response.data.keys()), sorted(['id']))
    self.assertEqual(response.data['id'], self.channel.id)


#class PrivelegedTests(AuthenticatedAPITestCase):
#  pass


class UPCTests(AuthenticatedAPITestCase):

  def run_upc_test(self, upc):
    response = self.client.get("/api/upcs/?upc={}".format(upc), {}, **self.headers)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    if remote_lookup(upc) is not None:
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
