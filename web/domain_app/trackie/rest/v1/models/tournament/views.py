from rest_framework.viewsets import ModelViewSet
from .serializers import TournamentSerializer
from ......trackie.models import Tournament


class TournamentViewSet(ModelViewSet):
    serializer_class = TournamentSerializer
    queryset = Tournament.objects.all()
    lookup_field = "slug"
    lookup_value_regex = "[-_\w]+"

    def list(self, request, *args, **kwargs):
        return super(TournamentViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(TournamentViewSet, self).retrieve(
            request,
            *args,
            **kwargs
        )