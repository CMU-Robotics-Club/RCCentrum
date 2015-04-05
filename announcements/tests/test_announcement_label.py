from django.test import TestCase
from announcements.models import Announcement
from django.contrib.auth.models import User
from robocrm.models import RoboUser

class AnnouncementLabelTests(TestCase):
  
  def test_get_label_superuser_admin(self):
    """
    Should be able to get label through admin interface.
    """

    password = 'test'
    user = User.objects.create_superuser(username="bstrysko", email="test@gmail.com", password=password)
    robouser = RoboUser.objects.create(user=user)

    announcement = Announcement.objects.create(header="Header", body="Body", updater_object=robouser)

    self.assertTrue(self.client.login(username=user.username, password=password))

    response = self.client.get("/admin/announcements/announcement/{}/tools/create_announcement_label/".format(announcement.id))
    self.assertEqual(response.status_code, 200)
