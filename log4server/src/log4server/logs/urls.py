from django.conf.urls.defaults import patterns
from views import alert, status, register

urlpatterns = patterns(
    '',
    (r'^$', alert),
    (r'^status/', status),
    (r'^register/', register),
)

