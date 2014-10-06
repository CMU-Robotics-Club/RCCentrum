from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models.signals import post_save
from django.conf import settings

# Machine Model
class Machine(models.Model):
  type = models.CharField(max_length=20)
  id = models.CharField(max_length=10, primary_key=True)
  maint = models.BooleanField(default=False)
  dstart = models.DateTimeField(blank=True, null=True)
  dend = models.DateTimeField(blank=True, null=True)
  
  def __str__(self):
    return "{} {}".format(self.type, self.id)


class RoboUser(models.Model):
  # Field is required when using profiles 
  user = models.OneToOneField(User)

  # Roboclub Magnetic Card Number
  magnetic = models.CharField(max_length=9, null=True, unique=True)

  # Roboclub RFID Card Number
  rfid = models.CharField(max_length=10, null=True, unique=True)
  
  # Roboclub Shop Access Permissions
  machines = models.ManyToManyField(Machine, blank=True, null=True)

  # Cell Phone
  cell = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)

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

  # Primary and Secondary Major/Minors
  major = models.CharField(max_length=20)
  sec_major_one = models.CharField(max_length=20, blank=True, null=True)
  sec_major_two = models.CharField(max_length=20, blank=True, null=True)
  
  # Roboclub Transaction Info
  dues_paid = models.DateField(blank=True, null=True)
  tshirt_rec = models.BooleanField(default=False)
  
  # Shop and E-Bench Status
  GOOD = 'GD'
  FIRST_WARN = 'FS'
  SECOND_WARN = 'SD'
  SEM_BAN = 'SB'
  CLUB_BAN = 'CB'
  STATUS_CHOICES = (
      (GOOD, 'Good Standing'),
      (FIRST_WARN, 'First Warning Recieved'),
      (SECOND_WARN, 'Second Warning Recieved'),
      (SEM_BAN, 'Semester Ban'),
      (CLUB_BAN, 'Club Ban')
  )
  bench_status = models.CharField(max_length=2,
                                  choices=STATUS_CHOICES,
                                  default=GOOD)
  shop_status = models.CharField(max_length=2,
                                 choices=STATUS_CHOICES,
                                 default=GOOD)

  class Meta:
    ordering = ['user__username']

  def __str__(self):
    return self.user.username


# TODO: move to Tooltron
# Event Model
class Event(models.Model):
  type = models.CharField(max_length=30)
  tstart = models.DateTimeField()
  tend = models.DateTimeField()
  user = models.ForeignKey('RoboUser', null=True)
  succ = models.BooleanField(default=False)
  imgurl = models.URLField()
  machine = models.ForeignKey('Machine')
  matuse = models.TextField()
  
  def __str__(self):
    return "{} {} {}".format(self.type, 
      self.user.user.username if self.user else 'unknown', self.succ)
