from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^all/$', views.all, name="all"),
    url(r'^$', views.index, name='Index'),
    url(r'/search', views.search, name='Search'),
    url(r'/dsearch', views.dynamic_search, name="JSON Results"),
    url(r'^plan_surgery/$', views.plan_surgery, name='Plan Surgery'),
]
