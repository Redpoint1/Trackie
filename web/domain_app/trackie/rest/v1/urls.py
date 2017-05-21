""" Rest api urls v1 for domain """

from django.conf.urls import url
from rest_framework import routers

from .models.race_data.views import RaceDataViewSet, RaceDataReplayViewSet
from .models.race.views import (RaceViewSet, TournamentRacesViewSet, RaceOnlineViewSet, RaceDoneViewSet,
                                RaceUpcomingViewSet)
from .models.race_type.views import RaceTypeViewSet
from .models.sport_type.views import SportTypeViewSet, TournamentInSportType
from .models.track.views import TrackViewSet
from .models.tournament.views import TournamentViewSet
from .models.racer.views import RacerViewSet
from .models.projection.views import ProjectionViewSet
from .models.search.views import SearchViewSet
from .models.racer_in_race.views import RacerFinishedRace, RacerRacingRace, RacerUpcomingRace, ParticipantsRaceView
from .models.field_type.views import FieldTypeViewSet
from .models.token.views import AuthTokenView


router = routers.SimpleRouter()

router.register(
    r'races/(?P<race_pk>\d+)/data',
    RaceDataViewSet,
    base_name="racedata",
)

router.register(
    r'races/(?P<race_pk>\d+)/replay',
    RaceDataReplayViewSet,
    base_name="racereplay",
)

router.register(
    r'races',
    RaceViewSet,
    base_name="race",
)

router.register(
    r'races/online',
    RaceOnlineViewSet,
    base_name="online-race",
)

router.register(
    r'races/finished',
    RaceDoneViewSet,
    base_name="finished-race",
)

router.register(
    r'races/upcoming',
    RaceUpcomingViewSet,
    base_name="upcoming-race",
)

router.register(
    r'race-types',
    RaceTypeViewSet,
    base_name="racetype",
)

router.register(
    r'sport-types',
    SportTypeViewSet,
    base_name="sporttype",
)

router.register(
    r'sport-types/(?P<sport_slug>[-_\w]+)/tournaments',
    TournamentInSportType,
    base_name="sport-tournaments",
)

router.register(
    r'tracks',
    TrackViewSet,
    base_name="track",
)

router.register(
    r'tournaments',
    TournamentViewSet,
    base_name="tournament",
)

router.register(
    r'racers',
    RacerViewSet,
    base_name="racer",
)

router.register(
    r'projections',
    ProjectionViewSet,
    base_name="projection",
)

router.register(
    r'tournaments/(?P<id>[\d]+)/races',
    TournamentRacesViewSet,
    base_name="tournament-races",
)

router.register(
    r'search',
    SearchViewSet,
    base_name="search",
)

router.register(
    r'races/racer/(?P<racer_id>[\d]+)/finished',
    RacerFinishedRace,
    base_name="races-racer-finished",
)

router.register(
    r'races/racer/(?P<racer_id>[\d]+)/active',
    RacerRacingRace,
    base_name="races-racer-active",
)

router.register(
    r'races/racer/(?P<racer_id>[\d]+)/upcoming',
    RacerUpcomingRace,
    base_name="races-racer-upcoming",
)

router.register(
    r'field-types',
    FieldTypeViewSet,
    base_name="field-types",
)

urlpatterns = router.urls

urlpatterns += [
    url(r'^races/(?P<pk>\d+)/participants/$',
        view=ParticipantsRaceView.as_view(),
        name=ParticipantsRaceView.name
        ),
    url(r'^api-key/$',
        view=AuthTokenView.as_view(),
        name=AuthTokenView.name
        )
]
