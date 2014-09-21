from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'crm.views.home', name='home'),
    # url(r'^crm/', include('crm.foo.urls')),
    url(r'^roboauth/(?P<rfid_tag>[0-9A-Fa-f]+)/(?P<mach_num>\d+)/', 'robocrm.views.roboauth'),
    url(r'^roboauth/(?P<rfid_tag>[0-9A-Fa-f]+)/', 'robocrm.views.roboauthall'),
    url(r'^add_card_event/', 'robocrm.views.add_card_event'),

    url(r'^officers/', include('officers.urls')),
    url(r'^projects/', include('projects.urls')),
    url(r'^webcams/', include('webcams.urls')),
    url(r'^api/', include('api.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^tinymce/', include('tinymce.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
