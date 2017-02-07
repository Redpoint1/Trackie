""" Rest api urls v1 for domain """

from django.conf.urls import url
from rest_framework import routers

from . import views as trackie_rest_v1_views
from .models.racedata import RaceDataViewSet

router = routers.SimpleRouter()
router.register(
    r'race/(?P<race_pk>\d+)/data',
    RaceDataViewSet,
    base_name="racedata",
)

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
    url(r'^sport-types/$',
        view=trackie_rest_v1_views.SportTypesEndpoint.as_view(),
        name=trackie_rest_v1_views.SportTypesEndpoint.name
        ),
    url(r'^sport-type/(?P<slug>[-_\w]+)$',
        view=trackie_rest_v1_views.SportTypeEndpoint.as_view(),
        name=trackie_rest_v1_views.SportTypeEndpoint.name
        ),
    url(r'^tracks/$',
        view=trackie_rest_v1_views.TracksEndpoint.as_view(),
        name=trackie_rest_v1_views.TracksEndpoint.name
        ),
    url(r'^track/(?P<slug>[-_\w]+)$',
        view=trackie_rest_v1_views.TrackEndpoint.as_view(),
        name=trackie_rest_v1_views.TrackEndpoint.name
        ),
    url(r'^tournaments/$',
        view=trackie_rest_v1_views.TournamentsEndpoint.as_view(),
        name=trackie_rest_v1_views.TournamentsEndpoint.name
        ),
    url(r'^tournament/(?P<slug>[-_\w]+)$',
        view=trackie_rest_v1_views.TournamentEndpoint.as_view(),
        name=trackie_rest_v1_views.TournamentEndpoint.name
        ),
    url(r'^tournament/(?P<slug>[-_\w]+)/races$',
        view=trackie_rest_v1_views.TournamentRacesEndpoint.as_view(),
        name=trackie_rest_v1_views.TournamentRacesEndpoint.name
        ),
    url(r'^racer/(?P<pk>[\d]+)$',
        view=trackie_rest_v1_views.RacerEndpoint.as_view(),
        name=trackie_rest_v1_views.RacerEndpoint.name
        ),
    url(r'^projection/(?P<pk>[\d]+)$',
        view=trackie_rest_v1_views.ProjectionEndpoint.as_view(),
        name=trackie_rest_v1_views.ProjectionEndpoint.name
        ),
]

urlpatterns += router.urls
