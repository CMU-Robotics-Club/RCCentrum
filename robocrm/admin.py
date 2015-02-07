from robocrm.models import Machine
from django.forms import ModelForm, ValidationError
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth.forms import UserCreationForm
from robocrm.models import RoboUser
from django import forms
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin, FlatpageForm
from .util import subscribe_to_list
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django_object_actions import DjangoObjectActions
from django.conf import settings
from django.http import HttpResponse
from .label import create_robouser_label
from datetime import timedelta


class IsSetListFilter(admin.SimpleListFilter):
  """
  Filter used by is_magnetic_set and is_rfid_set
  """

  empty_value = None

  def lookups(self, request, model_admin):
    return (
      ('true', "True"),
      ('false', "False"),
    )

  def queryset(self, request, queryset):
    if(self.value()):
      v = (self.value() == "true")

      if v:
        return queryset.exclude(**{self.parameter_name: self.empty_value})
      else:
        return queryset.filter(**{self.parameter_name: self.empty_value})
    else:
      return queryset


class IsMagneticSetListFilter(IsSetListFilter):
  title = ('Is Magnetic Set')
  parameter_name = 'robouser__magnetic'


class IsRFIDSetListFilter(IsSetListFilter):
  title = ('Is RFID Set')
  parameter_name = 'robouser__rfid'


class IsMembershipValidListFilter(admin.SimpleListFilter):
  title = ('Is Membership Valid')
  parameter_name = 'robouser__membership_valid'
  
  def lookups(self, request, model_admin):
    return (
      ('true', "True"),
      ('false', "False"),
    )

  def queryset(self, request, queryset):
    if(self.value()):
      v = (self.value() == "true")

      exclude_ids = []
      
      for user in queryset:
        if user.robouser.membership_valid != v:
          exclude_ids.append(user.id)

      return queryset.exclude(id__in=exclude_ids)
    else:
      return queryset


class RoboUserInline(admin.StackedInline):

  model = RoboUser
  can_delete = False
  filter_horizontal = ('machines', )
  readonly_fields = ('is_magnetic_set', 'is_rfid_set', 'membership_valid', 'machines_authorized', 'machines_not_authorized', 'balance', 'club_activity', )

  def get_fields(self, request, obj=None):
    if obj:
      fields = super().get_fields(request, obj)

      # TODO: find better way to work around lazy behavior of user object
      # Unwrap SimpleLazyObject so type is 'User' or 'Project'
      user = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user

      if user != obj:
        fields.remove("magnetic")

      user = request.user
      if not user.is_superuser and not user.groups.filter(name='officers').exists():
        fields.remove('machines')

      return fields
    else:
      # New User
      return ('class_level', 'grad_year', 'major', 'dues_paid_year', )

  def membership_valid(self, obj):
    return obj.membership_valid
  membership_valid.boolean = True

  def is_magnetic_set(self, obj):
    return obj.is_magnetic_set
  is_magnetic_set.boolean = True

  def is_rfid_set(self, obj):
    return obj.is_rfid_set
  is_rfid_set.boolean = True

  def machines_authorized(self, obj):
    field = ""

    for i, machine in enumerate(obj.machines.all()):
      if i != 0:
        field += '<br />'

      field += str(machine)
      field += ' <img src="{}" />'.format("/static/admin/img/icon-yes.gif")

    return field
  machines_authorized.mark_safe=True

  def machines_not_authorized(self, obj):
    machines = Machine.objects.exclude(robouser=obj)
    field = ""

    for i, machine in enumerate(machines):
      if i != 0:
        field += '<br />'

      field += str(machine)
      field += ' <img src="{}" />'.format("/static/admin/img/icon-no.gif")

    return field
  machines_not_authorized.mark_safe=True

  def club_activity(self, obj):
    activities = obj.club_activity
    field = ""

    for i, activity in enumerate(activities):
      endpoint = activity.endpoint.rsplit("/")
      endpoint[:] = (x for x in endpoint if x != "")
      endpoint = endpoint[-1]
      created_datetime = activity.created_datetime

      # TODO: fix this hacky solution
      # Django and standard python treat timezones
      # differently it appears, so manually subtracted
      # 5 hours to make time correct
      created_datetime += timedelta(hours=-5)
      
      created_datetime_s = created_datetime.strftime("%A %B %d %Y, %I:%M:%S %p")
      s = "{}: {} {}".format(created_datetime_s, activity.updater_object, endpoint)

      if activity.extra:
        s += "({})".format(activity.extra)

      if activity.meta:
        s += " {}".format(activity.meta)

      s += " Granted" if activity.success else " Denied" 

      field += "{} | <a href='{}'>Details</a> <br />".format(s, reverse('admin:api_apirequest_change', args=(activity.id,)))

    return field
  club_activity.mark_safe=True
  club_activity.short_description="Club Activity(most recent 15 events)"

  def get_readonly_fields(self, request, obj=None):
    if obj:
      user = request.user

      if not user.is_superuser and not user.groups.filter(name='officers').exists():
        return super().get_readonly_fields(request, obj) + ('rfid_card', 'rfid', 'dues_paid', 'dues_paid_year', )
      else:
        return super().get_readonly_fields(request, obj)
    else:
      return super().get_readonly_fields(request, obj)


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


class RoboUserAdmin(DjangoObjectActions, admin.ModelAdmin):
  inlines = (RoboUserInline, )
  list_display = ('username', 'email', 'first_name', 'last_name', 'is_superuser', 'roles', 'last_login', 'date_joined', 'dues_paid', 'dues_paid_year', 'membership_valid', 'is_magnetic_set', 'is_rfid_set', 'rfid_card', 'class_level', 'major', 'grad_year', 'balance', )
  search_fields = ['username', 'email', 'first_name', 'last_name', 'last_login', 'date_joined', ]
  exclude = ['password', 'user_permissions', 'is_active', 'is_staff', ]
  filter_horizontal = ('groups',)
  list_filter = ('is_superuser', 'robouser__dues_paid_year', IsMembershipValidListFilter, IsMagneticSetListFilter, IsRFIDSetListFilter, 'robouser__rfid_card', 'robouser__class_level', 'robouser__major', 'robouser__grad_year', )

  def create_robouser_label(self, request, obj):
    response = HttpResponse(content_type="image/png")
    image = create_robouser_label(obj)
    image.save(response, "PNG")
    return response
  create_robouser_label.label = "<i class='icon-picture icon-alpha75'></i>Create RoboUser Label"

  objectactions = ('create_robouser_label', )


  def is_magnetic_set(self, obj):
    return obj.robouser.is_magnetic_set
  is_magnetic_set.boolean = True

  def is_rfid_set(self, obj):
    return obj.robouser.is_rfid_set
  is_rfid_set.boolean = True

  def rfid_card(self, obj):
    return obj.robouser.rfid_card

  def class_level(self, obj):
    return obj.robouser.class_level

  def major(self, obj):
    return obj.robouser.major

  def grad_year(self, obj):
    return obj.robouser.grad_year

  def dues_paid(self, obj):
    return obj.robouser.dues_paid

  def dues_paid_year(self, obj):
    return obj.robouser.dues_paid_year
  dues_paid_year.boolean = True

  def membership_valid(self, obj):
    return obj.robouser.membership_valid
  membership_valid.boolean = True

  def balance(self, obj):
    return obj.robouser.balance

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
      fields = ['last_login', 'date_joined', 'username', 'first_name', 'last_name', 'email', ]

      if request.user == obj:
        fields.remove('first_name')
        fields.remove('email')

      return fields
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

  def get_actions(self, request):
    actions = super().get_actions(request)
    del actions['delete_selected']
    return actions

  def has_delete_permission(self, request, obj=None):
    return False

  class Meta:
    ordering = ['username']
    order_with_respect_to = 'username'


class MachineAdmin(admin.ModelAdmin):
   list_display = ('id', 'type', )


class GroupAdmin(GroupAdmin):
  list_display = ['name', 'members']
  list_display_links = ['name']

  def members(self, obj):
    return ', '.join(['<a href="%s">%s</a>' % (reverse('admin:auth_user_change', args=(x.id,)), x.username) for x in obj.user_set.all().order_by('username')])
  members.allow_tags = True


admin.site.unregister(User)
admin.site.register(User, RoboUserAdmin)
admin.site.register(Machine, MachineAdmin)

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
