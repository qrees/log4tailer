from django.conf.urls.defaults import patterns, include
from django.conf.urls import defaults
#from log4server.logs.views import alert, status, register
from log4server import settings

urlpatterns = patterns(
    '',
    (r'^alerts/$', 'log4server.logs.views.alert'),
    (r'^alerts/status/', 'log4server.logs.views.status'),
    (r'^alerts/search/', 'log4server.logs.views.search'),
    (r'^register/', 'log4server.logs.views.register'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),

)

handler404 = defaults.handler404
handler500 = defaults.handler500

