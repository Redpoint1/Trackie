""" Rest api urls v1 for domain """

from django.conf.urls import url

from . import views as trackie_rest_v1_views

urlpatterns = [  # pylint: disable=invalid-name
    url(r'^races/$',
        view=trackie_rest_v1_views.RacesEndpoint.as_view(),
        name=trackie_rest_v1_views.RacesEndpoint.name
        ),
    url(r'^race/(?P<pk>\d+)$',
        view=trackie_rest_v1_views.RaceEndpoint.as_view(),
        name=trackie_rest_v1_views.RaceEndpoint.name
        ),
    url(r'^race-types/$',
        view=trackie_rest_v1_views.RaceTypesEndpoint.as_view(),
        name=trackie_rest_v1_views.RaceTypesEndpoint.name
        ),
    url(r'^race-type/(?P<slug>[-_\w]+)$',
        view=trackie_rest_v1_views.RaceTypeEndpoint.as_view(),
        name=trackie_rest_v1_views.RaceTypeEndpoint.name
        ),
    url(r'^tracks/$',
        view=trackie_rest_v1_views.TracksEndpoint.as_view(),
        name=trackie_rest_v1_views.TracksEndpoint.name
        ),
    url(r'^track/(?P<slug>[-_\w]+ )$',
        view=trackie_rest_v1_views.TrackEndpoint.as_view(),
        name=trackie_rest_v1_views.TrackEndpoint.name
        ),
]
