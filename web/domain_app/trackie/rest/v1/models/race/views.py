from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import RaceSerializer, ShortRaceSerializer
from ......trackie.models import Race, Tournament
from ....permissions import IsOwnerOrReadOnly, NotProtectedOrReadOnly


class RaceViewSet(ModelViewSet):
    serializer_class = RaceSerializer
    queryset = Race.objects.all()
    permission_classes = (IsOwnerOrReadOnly, NotProtectedOrReadOnly,)
    trackie_owner = "tournament.owner"
    trackie_protect = "data"
    trackie_protect_methods = ("PUT", "PATCH", "DELETE")
    lookup_value_regex = "\d+"

    def list(self, request, *args, **kwargs):
        self.serializer_class = ShortRaceSerializer
        return super(RaceViewSet, self).list(request, *args, **kwargs)


class RaceOnlineViewSet(ReadOnlyModelViewSet):
    serializer_class = ShortRaceSerializer
    queryset = Race.objects.filter(real_start__isnull=False, real_end__isnull=True)


class RaceDoneViewSet(ReadOnlyModelViewSet):
    serializer_class = ShortRaceSerializer
    queryset = Race.objects.filter(real_start__isnull=False, real_end__isnull=False)


class RaceUpcomingViewSet(ReadOnlyModelViewSet):
    serializer_class = ShortRaceSerializer
    queryset = Race.objects.filter(real_start__isnull=True, real_end__isnull=True)


class OwnRaceViewSet(ReadOnlyModelViewSet):
    serializer_class = ShortRaceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Race.objects.filter(tournament__owner=self.request.user.pk)


class TournamentRacesViewSet(ModelViewSet):
    serializer_class = RaceSerializer

    def list(self, request, *args, **kwargs):
        self.serializer_class = ShortRaceSerializer
        return super(TournamentRacesViewSet, self).list(
            request,
            *args,
            **kwargs
        )

    def get_queryset(self):
        return Tournament.objects.get(**self.kwargs).races.all()
