from django.conf.urls.defaults import patterns, include
from django.conf.urls import defaults

urlpatterns = patterns(
    '',
    (r'^alerts/', include('log4server.logs.urls')),
)

handler404 = defaults.handler404
handler500 = defaults.handler500

