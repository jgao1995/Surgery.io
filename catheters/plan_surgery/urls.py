from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^all/$', views.all, name="all"),
    url(r'^add_device/$', views.show_add_device_1, name="Add Device"),
    url(r'^add_device_2/$', views.show_add_device_2, name="Add Device2"),
    url(r'^submit_device/$', views.add_device, name="Add Device Post"),
    url(r'^$', views.index, name='Index'),
    url(r'/search', views.search, name='Search'),
    url(r'/dsearch', views.dynamic_search, name="JSON Results"),
    url(r'^plan_surgery/$', views.plan_surgery, name='Plan Surgery'),
    url(r'^plan_surgery/new', views.new_surgery),
    url(r'^device/(?P<id>[0-9]+)/$', views.show, name='Device show'),
    url(r'^device/(?P<id>[0-9]+)/add_video', views.add_video),
    url(r'^device/(?P<id>[0-9]+)/add_comment$', views.add_comment),
]
