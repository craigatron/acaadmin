from django.conf.urls import patterns, url
from schedule import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='schedule_index'),
    url(r'^feed/?$', views.event_feed),
    url(r'^(?P<event_id>[0-9]+)/?$', views.event_view),
    url(r'^(?P<event_id>[0-9]+)/change/?$', views.change_attendance),
)
