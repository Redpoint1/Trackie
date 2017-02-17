from rest_framework.viewsets import ModelViewSet
from .serializers import RaceSerializer
from ......trackie.models import Race, Tournament


class RaceViewSet(ModelViewSet):
    serializer_class = RaceSerializer
    queryset = Race.objects.all()

    def list(self, request, *args, **kwargs):
        return super(RaceViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(RaceViewSet, self).retrieve(request, *args, **kwargs)


class TournamentRacesViewSet(ModelViewSet):
    serializer_class = RaceSerializer

    def list(self, request, *args, **kwargs):
        return super(TournamentRacesViewSet, self).list(
            request,
            *args,
            **kwargs
        )

    def get_queryset(self):
        return Tournament.objects.get(**self.kwargs).races.all()
