from django.conf.urls import url

from . import views

urlpatterns = [

    # INDEX
    url(r'^$', views.index, name='index'),

    # DEVICE MANAGEMENT
    # ADD DEVICE
    url(r'^add_device/$', views.show_add_device_1, name="Add Device"),
    url(r'^add_device_2/$', views.show_add_device_2, name="Add Device2"),
    url(r'^submit_device/$', views.add_device, name="Add Device Post"),


    # ALL DEVICES
    url(r'^all/$', views.all_devices, name="all"),
    url(r'^search$', views.search, name='Search'),
    url(r'^dsearch$', views.dynamic_search, name="JSON Results"),
    url(r'^device_search$', views.search_devices),

    # ADD DEVICE TYPE
    url(r'^add_device_type/$', views.add_device_type, name="add device type"),
    
    
    # PLAN SURGERY
    url(r'^plan_surgery/$', views.plan_surgery, name='Plan Surgery'),
    url(r'^plan_surgery/all$', views.all_surgeries, name='All Surgeries'),
    url(r'^plan_surgery/new', views.new_surgery),
    url(r'^plan_surgery/add_surgery', views.add_surgery),
    url(r'^surgery/(?P<id>[0-9]+)/$', views.show_surgery, name='Surgery show'),
    url(r'^device/(?P<id>[0-9]+)/$', views.show, name='Device show'),
    url(r'^device/(?P<id>[0-9]+)/JSON$', views.add_device_to_surgery),
    url(r'^device/(?P<id>[0-9]+)/add_video', views.add_video),
    url(r'^device/(?P<id>[0-9]+)/add_comment$', views.add_comment),

    # USERS
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name='logout'),

    # HELP
    url(r'^help/$', views.help, name="help"),
]
