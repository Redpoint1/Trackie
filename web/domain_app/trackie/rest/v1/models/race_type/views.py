from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import RaceTypeSerializer
from ......trackie.models import RaceType


class RaceTypeViewSet(ModelViewSet):
    serializer_class = RaceTypeSerializer
    queryset = RaceType.objects.all()


class OwnRaceTypeViewSet(ReadOnlyModelViewSet):
    serializer_class = RaceTypeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return RaceType.objects.filter(owner=self.request.user.pk)
