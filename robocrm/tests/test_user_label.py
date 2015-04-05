from django.test import TestCase
from django.contrib.auth.models import User
from robocrm.models import RoboUser

class RoboUserLabelTests(TestCase):
  
  def test_get_label_superuser_admin(self):
    """
    Should be able to get label through admin interface.
    """
    
    password = 'test'
    user = User.objects.create_superuser(username="bstrysko", email="test@gmail.com", password=password)
    robouser = RoboUser.objects.create(user=user)

    self.assertTrue(self.client.login(username=user.username, password=password))

    response = self.client.get("/admin/auth/user/{}/tools/create_robouser_label/".format(robouser.user.id))
    self.assertEqual(response.status_code, 200)
