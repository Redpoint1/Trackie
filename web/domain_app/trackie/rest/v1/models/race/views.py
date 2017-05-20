from rest_framework.viewsets import ModelViewSet
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

    def list(self, request, *args, **kwargs):
        self.serializer_class = ShortRaceSerializer
        return super(RaceViewSet, self).list(request, *args, **kwargs)


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
