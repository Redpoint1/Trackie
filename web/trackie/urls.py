""" Django basic/root urls """

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [  # pylint: disable=invalid-name
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('app.api.urls')),
    url(r'^', include('domain_app.trackie.urls')),
]

if settings.DEBUG:
    import debug_toolbar  # pylint: disable=wrong-import-position
    urlpatterns.append(
        url(r'^__debug__/', include(debug_toolbar.urls))
    )
