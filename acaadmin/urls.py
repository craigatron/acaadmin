from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'acaadmin.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^songs/', include('songs.urls')),
    url(r'^logout/?$', 'django.contrib.auth.views.logout'),
    url(r'^error/?$', 'django.views.defaults.permission_denied'),
    url('', include('social.apps.django_app.urls', namespace='social')),
)
