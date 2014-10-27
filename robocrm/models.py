from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models.signals import post_save
from django.conf import settings
from .fields import CharNullField

class Machine(models.Model):
  type = models.CharField(max_length=20)
  id = models.CharField(max_length=10, primary_key=True)
  maint = models.BooleanField(default=False)
  
  def __str__(self):
    return "{} {}".format(self.type, self.id)


class RoboUser(models.Model):
  # Field is required when using profiles 
  user = models.OneToOneField(User)

  # TODO: make these unique once null allowed char field is implemented
  # Roboclub Magnetic Card Number
  magnetic = CharNullField(max_length=9, null=True, blank=True, unique=True, help_text="9 Character Magnetic Card ID(found on Student ID)")

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

  major = models.CharField(max_length=20)
  
  # Roboclub Transaction Info
  dues_paid = models.DateField(blank=True, null=True)

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
