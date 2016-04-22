from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^all/$', views.all, name="all"),

    # DEVICE MANAGEMENT
    # ADD DEVICE
    url(r'^add_device/$', views.show_add_device_1, name="Add Device"),
    url(r'^add_device_2/$', views.show_add_device_2, name="Add Device2"),
    url(r'^submit_device/$', views.add_device, name="Add Device Post"),

    # ADD DEVICE TYPE
    url(r'^add_device_type/$', views.add_device_type, name="add device type"),

    url(r'^$', views.index, name='index'),
    url(r'/search', views.search, name='Search'),
    url(r'/dsearch', views.dynamic_search, name="JSON Results"),
    url(r'^plan_surgery/$', views.plan_surgery, name='Plan Surgery'),
    url(r'^device/(?P<id>[0-9]+)/$', views.show, name='Device show'),
    url(r'^device/(?P<id>[0-9]+)/add_video', views.add_video),
    url(r'^device/(?P<id>[0-9]+)/add_comment$', views.add_comment),

    # USERS
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name='logout'),
]
