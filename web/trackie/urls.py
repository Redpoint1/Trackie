""" Django basic/root urls """

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [  # pylint: disable=invalid-name
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^accounts/', include('allauth.urls')),
    url(r'^api/', include('app.api.urls')),
    url(r'^', include('domain_app.trackie.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    import debug_toolbar  # pylint: disable=wrong-import-position
    urlpatterns.append(
        url(r'^__debug__/', include(debug_toolbar.urls))
    )
    urlpatterns.extend(
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
