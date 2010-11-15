from django.conf.urls.defaults import *

# special urls for flatpage test cases
urlpatterns = patterns('',
    (r'^flatpage_root', include('flatpagesplus.urls')),
    (r'^accounts/', include('django.contrib.auth.urls')),
)

