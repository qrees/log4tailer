from django.conf.urls.defaults import patterns
from log4server.logs.views import alert 

urlpatterns = patterns(
    '',
    (r'^$', alert),
)

