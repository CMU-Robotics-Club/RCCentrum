from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models.signals import post_save
from django.conf import settings
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.core.validators import RegexValidator
from .fields import CharNullField
from api.models import APIRequest
from crm.models import TimeStampedModel

class Machine(TimeStampedModel):
  type = models.CharField(max_length=20)

  # TODO: figure out how to make a migration
  # removing this and making id an integer while
  # preserving existing data
  id = models.CharField(max_length=10, primary_key=True)

  toolbox_id = models.PositiveIntegerField(null=True, blank=True, default=None, unique=True)

  """
  True if a RFID is presently in the machine's RFID reader.
  """
  rfid_present = models.BooleanField(default=False)

  """
  Whose RFID is present.  None if no RFID present or unknown User.
  """
  user = models.ForeignKey('robocrm.RoboUser', null=True)

  """
  If the tool is powered on, detected via current sensing.
  """
  powered = models.BooleanField(default=False)

  def __str__(self):
    return self.type


class RoboUser(models.Model):
  # Field is required when using profiles 
  user = models.OneToOneField(User)

  # Roboclub Magnetic Card Number
  magnetic = CharNullField(max_length=9, null=True, blank=True, unique=True, help_text="9 Character Magnetic Card ID(found on Student ID)(Only you can see this ID)", validators=[
    RegexValidator(
      regex='^[0-9]{9}$',
      message='Magnetic must be 9 numeric characters(0-9)',
      code='invalid_magnetic'
    ),
  ])

  # Roboclub RFID Card Number
  rfid = CharNullField(max_length=10, null=True, blank=True, unique=True, validators=[
    RegexValidator(
      regex='^[A-F0-9]{8}$',
      message='RFID must be 8 hexadecimal characters(0-9, A-F)',
      code='invalid_rfid'
    ),
  ])

  RFID_CARD_CHOICES = (
      ("CMU", "CMU ID"),
      ("PITT", "PITT ID"),
      ("OTHER", "OTHER ID"),
  )
  rfid_card = models.CharField(max_length=5, 
                                 choices=RFID_CARD_CHOICES,
                                 default="CMU")

  @property
  def is_magnetic_set(self):
    return bool(self.magnetic)

  @property
  def is_rfid_set(self):
    return bool(self.rfid)
  
  # Roboclub Shop Access Permissions
  machines = models.ManyToManyField(Machine, blank=True, null=True, db_index=True)

  # Cell Phone
  cell = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, help_text="Cell Phone # if you wish to provide it to Officers")

  # Class Level
  UNDERGRAD = 'UG'
  GRADUATE = 'GR'
  AFFILIATE = 'AF'
  OTHER = 'OH'
  CLASS_LEVEL_CHOICES = (
      (UNDERGRAD, 'Undergraduate'),
      (GRADUATE, 'Graduate Student'),
      (AFFILIATE, 'Non-Student CMU Affiliate'),
      (OTHER, 'Other User'),
  )
  class_level = models.CharField(max_length=2, 
                                 choices=CLASS_LEVEL_CHOICES,
                                 default=UNDERGRAD)

  # Graduation Year
  grad_year = models.IntegerField(blank=True, null=True)

  major = models.CharField(max_length=50)
  
  # If someone trusts Roboclub with more than $999 we have a problem
  balance = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Roboclub balance(currently only being used by Fridgetron)")

  # Roboclub Transaction Info
  dues_paid = models.DateField()
  dues_paid_year = models.BooleanField(default=True, help_text="Unchecked if only Semester membership was paid")

  color = models.CharField(max_length=60, default="FF0000", help_text="Color (pattern, up to 10 colors,) that can be used by Projects(up to 60 hexadecimal characters)", validators=[
    RegexValidator(
      regex = '^(?:[0-9A-F]{6})+$',
      message='Must be a valid color code(multiple of 6 hexadecimal characters)(ex. "FF0000" is red, FF000000FF00 red-green pattern)',
      code='invalid_color'
    ),
  ])

  @property
  def membership_valid(self):
    """
    Returns True if membership is still valid,
    False otherwise(should pay dues).
    """

    today = date.today()

    if self.dues_paid is None:
      return False

    months = 12 if self.dues_paid_year else 6
    dues_due = datetime.combine(self.dues_paid, datetime.min.time()) + relativedelta(months=+months)
    dues_due = dues_due.date()

    return dues_due > today

  @property
  def club_activity(self):
    """
    Return up to the 15 most recent
    APIRequests for this user.
    """

    return APIRequest.objects.filter(user=self).order_by('-created_datetime')[:15]

  def save(self, *args, **kwargs):
    if self.dues_paid is None:
      self.dues_paid = date.today()

    return super().save(*args, **kwargs)

  class Meta:
    ordering = ['user__username']

  def __str__(self):
    return self.user.username
