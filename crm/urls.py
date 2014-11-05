from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from password_reset import views as password_reset_views
from django.http import HttpResponseRedirect

urlpatterns = patterns('',
    url(r'^officers/', include('officers.urls', namespace='officers')),
    url(r'^sponsors/', include('sponsors.urls', namespace='sponsors')),
    url(r'^projects/', include('projects.urls', namespace='projects')),
    url(r'^webcams/', include('webcams.urls', namespace='webcams')),
    url(r'^posters/', include('posters.urls', namespace='posters')),  
    url(r'^api/', include('api.urls')),

    url(r'^admin/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^tinymce/', include('tinymce.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Declare this url before password_reset.urls does so Django Suit
    # picks up the right URL name and add a 'Reset my password' link
    # in the login form.  If we do our own password reset instead of the app
    # we would not need to do this, but this is easier.
    url(r'^recover/$', password_reset_views.recover, name='admin_password_reset'),

    url(r'^', include('password_reset.urls')),
    url(r'^', include('robocrm.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
