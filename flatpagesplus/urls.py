from django.conf.urls.defaults import *

urlpatterns = patterns('flatpagesplus.views',
    (r'^(?P<url>.*)$', 'flatpage'),
)
