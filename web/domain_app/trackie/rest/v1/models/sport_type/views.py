from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from .serializers import SportTypeSerializer
from ..tournament.serializers import ShortTournamentSerializer
from ......trackie.models import SportType, Tournament


class SportTypeViewSet(ModelViewSet):
    serializer_class = SportTypeSerializer
    queryset = SportType.objects.all()
    lookup_field = "slug"
    lookup_value_regex = "[-_\w]+"

    def list(self, request, *args, **kwargs):
        return super(SportTypeViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(SportTypeViewSet, self).retrieve(request, *args, **kwargs)


class TournamentInSportType(ModelViewSet):
    serializer_class = ShortTournamentSerializer

    def get_queryset(self):
        sport_slug = self.kwargs.get("sport_slug")
        sport = get_object_or_404(SportType, slug=sport_slug)
        self.queryset = Tournament.objects.filter(sport_id=sport["id"])
        return super(TournamentInSportType, self).get_queryset()

    def list(self, request, *args, **kwargs):
        return super(TournamentInSportType, self).list(request, *args, **kwargs)
