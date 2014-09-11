from django.conf.urls import patterns, include, url
from robocrm.models import RoboUser
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User

from django.contrib import admin
from robocrm import views
admin.autodiscover()


#TODO: move this to better place

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', )

class RoboUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    # TODO: find better way to do this
    def to_native(self, obj):
        """
        Hack to embed 'user' fields into main object
        eliminating nested fields.
        """

        ret = super(RoboUserSerializer, self).to_native(obj)
        p_serializer = UserSerializer(obj.user, context=self.context)
        p_ret = p_serializer.to_native(obj.user)

        del p_ret['id']

        for key in p_ret:
            ret[key] = p_ret[key]

        del ret['user']

        return ret

    class Meta:
        model = RoboUser
        depth = 2

        #fields = (
        #   ('user', 'UserSerializer'),
        #)

class RoboUserViewSet(viewsets.ReadOnlyModelViewSet):
    model = RoboUser
    serializer_class = RoboUserSerializer

router = routers.DefaultRouter()
router.register(r'users', RoboUserViewSet)




urlpatterns = patterns('',
    # url(r'^$', 'crm.views.home', name='home'),
    # url(r'^crm/', include('crm.foo.urls')),
    url(r'^roboauth/(?P<rfid_tag>[0-9A-Fa-f]+)/(?P<mach_num>\d+)/', 'robocrm.views.roboauth'),
    url(r'^roboauth/(?P<rfid_tag>[0-9A-Fa-f]+)/', 'robocrm.views.roboauthall'),
    url(r'^add_card_event/', 'robocrm.views.add_card_event'),

    url(r'^api/v1/', include(router.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^tinymce/', include('tinymce.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)