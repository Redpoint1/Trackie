""" Rest api urls v1 for domain """

from django.conf.urls import url
from rest_framework import routers

from .models.race_data.views import RaceDataViewSet
from .models.race.views import RaceViewSet, TournamentRacesViewSet
from .models.race_type.views import RaceTypeViewSet
from .models.sport_type.views import SportTypeViewSet
from .models.track.views import TrackViewSet
from .models.tournament.views import TournamentViewSet
from .models.racer.views import RacerViewSet
from .models.projection.views import ProjectionViewSet


router = routers.SimpleRouter()

router.register(
    r'races/(?P<race_pk>\d+)/data',
    RaceDataViewSet,
    base_name="racedata",
)

router.register(
    r'races',
    RaceViewSet,
    base_name="race",
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
    r'tournaments/(?P<slug>[-_\w]+)/races',
    TournamentRacesViewSet,
    base_name="tournament-races",
)

urlpatterns = router.urls
