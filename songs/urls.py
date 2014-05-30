from django.conf.urls import patterns, url
from songs import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='songs_index'),
    url(r'^add/?$', views.add, name='songs_add'),
    url(r'^(?P<song_id>[^/]+)/delete$', views.delete, name='songs_delete'),
    url(r'^(?P<song_id>[^/]+)/vote/(?P<vote>[0-2x])$', views.vote, name='songs_vote'),
    url(r'^(?P<song_id>[^/]+)/arrange$', views.arrange, name='songs_arrange')
)
