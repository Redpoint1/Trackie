""" Rest api urls for each version """

from django.conf.urls import include, url

urlpatterns = [  # pylint: disable=invalid-name
    url(r'^v1/', include('app.api.rest.v1.urls')),
]
