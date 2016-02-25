from django.conf.urls import url

from . import views

urlpatterns = [
<<<<<<< HEAD
    url(r'^$', views.index, name='index'),
    url(r'/search', views.search)

]

=======
    url(r'^all/$', views.all, name="all"),
    url(r'^$', views.index, name='Index'),
    url(r'^plan_surgery/$', views.plan_surgery, name='Plan Surgery'),
]
>>>>>>> 3083c981b0408f060fced241f5a9f9b2396d0bd5
