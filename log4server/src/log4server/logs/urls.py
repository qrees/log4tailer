from django.conf.urls.defaults import patterns
from log4server.logs.views import alert, info

urlpatterns = patterns(
    '',
    (r'^$', alert),
    (r'^info/', info),
)

