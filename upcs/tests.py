from django.test import TestCase
from .format_upc import format_upc
from .remote_lookup import remote_lookup

class FormatUPCTests(TestCase):

  def test_upce_length_6(self):
    """
    6 digit UPCE to 8 digit UPCE
    """

    self.assertEquals(format_upc("404350"), "04043506")


  def test_upce_length_7(self):
    """
    7 digit UPCE to 8 digit UPCE
    """

    self.assertEquals(format_upc("0404350"), "04043506")


  def test_upca_length_12(self):
    """
    12 digit UPCA to 12 digit UPCA (unmodified)
    """

    upc = "044000037420"
    self.assertEquals(format_upc(upc), upc)

  def test_upc_unknown_length(self):
    """
    11 digit UPCA to None
    """

    self.assertEquals(format_upc("04400003742"), None)



class RemoteLookupTests(TestCase):

  def test_remote_lookup_upca(self):
    self.assertEquals(remote_lookup("04043506"), "TWIX Candy Bar")

  def test_remote_lookup_upce(self):
    self.assertEquals(remote_lookup("044000037420"), "Oreo Cookie")

  def test_remote_lookup_unknown(self):
    self.assertEquals(remote_lookup("010002000000"), None)
