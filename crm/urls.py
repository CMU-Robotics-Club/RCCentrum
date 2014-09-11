from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from robocrm import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'crm.views.home', name='home'),
    # url(r'^crm/', include('crm.foo.urls')),
    url(r'^roboauth/(?P<rfid_tag>[0-9A-Fa-f]+)/(?P<mach_num>\d+)/', 'robocrm.views.roboauth'),
    url(r'^roboauth/(?P<rfid_tag>[0-9A-Fa-f]+)/', 'robocrm.views.roboauthall'),
    url(r'^add_card_event/', 'robocrm.views.add_card_event'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
   
    (r'^tinymce/', include('tinymce.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
