from rest_framework.viewsets import ModelViewSet
from .serializers import TournamentSerializer
from ......trackie.models import Tournament


class TournamentViewSet(ModelViewSet):
    serializer_class = TournamentSerializer
    queryset = Tournament.objects.all()
