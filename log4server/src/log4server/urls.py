from django.conf.urls.defaults import patterns, include
from django.conf.urls import defaults

urlpatterns = patterns(
    '',
    (r'^alerts/', include('log4server.logs.urls')),
)
handler500 = defaults.handler500

