from robocrm.models import Machine, Event
from django.forms import ModelForm, ValidationError
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Permission, Group
from django.contrib.sites.models import Site
from django.contrib.auth.forms import UserCreationForm
from robocrm.models import RoboUser
from django import forms
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin, FlatpageForm
from .util import subscribe_to_list
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

class RoboUserInline(admin.StackedInline):
  model = RoboUser
  can_delete = False
  filter_horizontal = ('machines', )

  # TODO: find a way to make Django not abbreviate the result
  # of 'Machine.objects.exclude(robouser=obj)' so the string
  # does not manually need to be constructed.
  # Displays '[,,,,,,]' if string not manually constructed)
  def machines_not_authorized(self, obj):
    machines = Machine.objects.exclude(robouser=obj)
    field = ""

    for i, machine in enumerate(machines):
      if i != 0:
        field += ', '

      field += str(machine)

    return field

  def get_readonly_fields(self, request, obj=None):
    if obj:
      user = request.user

      if not user.is_superuser and not user.groups.filter(name='officers').exists():
        return ['machines', 'machines_not_authorized', 'rfid', 'dues_paid']
      else:
        return []
    else:
      return super().get_readonly_fields(request, obj)

  def get_fieldsets(self, request, obj=None):
    if obj:
      user = request.user

      if not user.is_superuser and not user.groups.filter(name='officers').exists():
        return (
          (None, {'fields':
            ('cell', 'machines', 'machines_not_authorized', 'magnetic', 'rfid', 'class_level', 'major', 'grad_year', 'dues_paid') 
          }),
        )
      else:
        return super().get_fieldsets(request, obj)
    else:
      # add user form
      return (
          (None, {'fields':
            ('class_level', 'grad_year', 'major', 'dues_paid',
            )
          }),)

class UserCreationForm(ModelForm):

  def clean_username(self):
    username = self.cleaned_data['username']
    try:
      User.objects.get(username=username)
    except User.DoesNotExist:
      return username
    raise ValidationError('Username already exists')

  def save(self, commit=True):
    user = super().save(commit=False)
    user.set_password(User.objects.make_random_password())
    user.is_staff = True

    # Hacky but only way to get default groups to work since
    # original save_m2m overrides groups
    old_save_m2m = self.save_m2m
    def save_m2m():
      old_save_m2m()
      members_group = Group.objects.get_or_create(name='members')[0]
      user.groups.clear()
      user.groups.add(members_group)
    self.save_m2m = save_m2m

    if commit:
      user.save()

    # TODO: make this mailing list a setting
    subscribe_to_list(user.first_name, user.last_name, user.email, 'roboclub-gb')
    return user

  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', )

  class Media:
    js = (
      'jquery-1.11.1.min.js',
      'robocrm/js/cmu.js',
      'robocrm/js/cmu_directory.js',
    )


class RoboUserAdmin(admin.ModelAdmin):
  inlines = (RoboUserInline, )
  list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_superuser', 'roles', 'last_login', 'date_joined', 'dues_paid', 'is_magnetic_set', 'is_rfid_set', 'class_level', 'major', 'grad_year', )
  search_fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'last_login', 'date_joined', ]
  exclude = ['password', 'user_permissions', 'is_staff', ]
  filter_horizontal = ('groups',)

  def is_magnetic_set(self, obj):
    return obj.robouser.is_magnetic_set
  is_magnetic_set.boolean = True

  def is_rfid_set(self, obj):
    return obj.robouser.is_rfid_set
  is_rfid_set.boolean = True

  def class_level(self, obj):
    return obj.robouser.class_level

  def major(self, obj):
    return obj.robouser.major

  def grad_year(self, obj):
    return obj.robouser.grad_year

  def dues_paid(self, obj):
    return obj.robouser.dues_paid

  def roles(self, obj):
    p = sorted([str(x) for x in obj.groups.all()])
    if obj.user_permissions.count():
      p += ['+']
    value = ', '.join(p)
    return mark_safe("<nobr>{}</nobr>".format(value))
  roles.allow_tags = True
  roles.short_description = 'Groups'

  def get_readonly_fields(self, request, obj=None):
    if obj:
      return ['last_login', 'date_joined', 'username', 'first_name', 'last_name', 'email', ]
    else:
      return []

  def get_form(self, request, obj=None, **kwargs):
    if obj:
      return super().get_form(request, obj, **kwargs)
    else:
      return UserCreationForm

  def get_fieldsets(self, request, obj=None):
    if obj:
      user = request.user
  
      if not user.is_superuser and not user.groups.filter(name='officers').exists():
        return (
          (None, {'fields':
            ('username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined', )
          }),
        )
      else:
        return super().get_fieldsets(request, obj)
    else:
      #return (None, {'fields':
      #  ('username', 'first_name', 'last_name', 'email', )
      #}),
      return super().get_fieldsets(request, obj)

  def get_queryset(self, request):
    qs = super().get_queryset(request)

    user = request.user

    # If not an superuser/officer only
    # let User only edit own information
    if not user.is_superuser and not user.groups.filter(name='officers').exists():
      qs = qs.filter(id=user.id)

    return qs

  class Meta:
    ordering = ['username']
    order_with_respect_to = 'username'

class EventAdmin(admin.ModelAdmin):
    list_display = ('type', 'tstart', 'tend', 'user', 'succ', 'machine', )
    readonly_fields = ('type', 'tstart', 'tend', 'user', 'succ', 'machine', )

    def has_add_permission(self, request):
      return False

class MachineAdmin(admin.ModelAdmin):
   list_display = ('type', 'maint', )
   readonly_fields = ('id', )

class GroupAdmin(GroupAdmin):
  list_display = ['name', 'members']
  list_display_links = ['name']

  def members(self, obj):
    return ', '.join(['<a href="%s">%s</a>' % (reverse('admin:auth_user_change', args=(x.id,)), x.username) for x in obj.user_set.all().order_by('username')])
  members.allow_tags = True

admin.site.unregister(User)
admin.site.register(User, RoboUserAdmin)
admin.site.register(Machine, MachineAdmin)
admin.site.register(Event, EventAdmin)

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
