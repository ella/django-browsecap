from django.conf.urls.defaults import *

from browsecap.sample import views

urlpatterns = patterns('',
    url(r'^$', views.homepage, name='browsecap-homepage'),
)

