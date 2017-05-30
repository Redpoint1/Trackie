from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import TournamentSerializer
from ......trackie.models import Tournament


class TournamentViewSet(ModelViewSet):
    serializer_class = TournamentSerializer
    queryset = Tournament.objects.all()


class OwnTournamentViewSet(ReadOnlyModelViewSet):
    serializer_class = TournamentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Tournament.objects.filter(owner=self.request.user.pk)
