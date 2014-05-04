from django.conf.urls import patterns, url
from songs import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='songs_index'),
    url(r'^add/?$', views.add, name='songs_add'),
    url(r'^(?P<song_id>[^/]+)/delete$', views.delete, name='songs_delete'),
)
