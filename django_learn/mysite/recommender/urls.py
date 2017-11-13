from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.recommender, name='recommender'),
    url(r'^sl$', views.sl, name='sl'),
    url(r'^us$', views.us, name='us'),
    url(r'^it$', views.it, name='it'),
    url(r'^sv$', views.sv, name='sv'),
    url(r'^svp$', views.svp, name='svp'),
]
