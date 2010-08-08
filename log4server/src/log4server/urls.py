from django.conf.urls.defaults import patterns, include
from django.conf.urls import defaults
from log4server.logs.views import alert, status, register

urlpatterns = patterns(
    '',
    (r'^alerts/$', alert),
    (r'^alerts/status/', status),
    (r'^register/', register),
)

handler404 = defaults.handler404
handler500 = defaults.handler500

