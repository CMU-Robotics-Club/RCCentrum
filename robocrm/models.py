from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models.signals import post_save
from django.conf import settings
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from .fields import CharNullField

class Machine(models.Model):
  type = models.CharField(max_length=20)

  # TODO: remove ID
  id = models.CharField(max_length=10, primary_key=True)
  
  maint = models.BooleanField(default=False)
  
  def __str__(self):
    return self.type


class RoboUser(models.Model):
  # Field is required when using profiles 
  user = models.OneToOneField(User)

  # Roboclub Magnetic Card Number
  magnetic = CharNullField(max_length=9, null=True, blank=True, unique=True, help_text="9 Character Magnetic Card ID(found on Student ID)(Only you can see this ID)")

  # Roboclub RFID Card Number
  rfid = CharNullField(max_length=10, null=True, blank=True, unique=True)

  def magnetic_set(self):
    return bool(self.magnetic)

  @property
  def is_magnetic_set(self):
    return bool(self.magnetic)

  @property
  def is_rfid_set(self):
    return bool(self.rfid)
  
  # Roboclub Shop Access Permissions
  machines = models.ManyToManyField(Machine, blank=True, null=True)

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
  #grad_year = models.DecimalField(max_digits=4, decimal_places=0)
  grad_year = models.IntegerField(blank=True, null=True)

  major = models.CharField(max_length=50)
  
  # Roboclub Transaction Info
  dues_paid = models.DateField()
  dues_paid_year = models.BooleanField(default=True, help_text="Unchecked if only Semester membership was paid")

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

  def save(self, *args, **kwargs):
    if self.dues_paid is None:
      self.dues_paid = date.today()

    return super().save(*args, **kwargs)

  class Meta:
    ordering = ['user__username']

  def __str__(self):
    return self.user.username


# TODO: move to Tooltron
class Event(models.Model):
  type = models.CharField(max_length=30)
  tstart = models.DateTimeField()
  tend = models.DateTimeField()
  user = models.ForeignKey('RoboUser', null=True)
  succ = models.BooleanField(default=False)
  machine = models.ForeignKey('Machine')
  
  def __str__(self):
    return "{} {} {}".format(self.type, 
      self.user.user.username if self.user else 'unknown', self.succ)
