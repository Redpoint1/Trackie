from rest_framework.viewsets import ModelViewSet
from .serializers import RaceTypeSerializer
from ......trackie.models import RaceType


class RaceTypeViewSet(ModelViewSet):
    serializer_class = RaceTypeSerializer
    queryset = RaceType.objects.all()
