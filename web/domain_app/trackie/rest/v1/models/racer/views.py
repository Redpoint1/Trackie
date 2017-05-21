from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import RacerSerializer, ShortRacerSerialiter
from ......trackie.models import Racer


class RacerViewSet(ModelViewSet):
    serializer_class = RacerSerializer
    queryset = Racer.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request, *args, **kwargs):
        self.serializer_class = ShortRacerSerialiter
        return super(RacerViewSet, self).list(request, *args, **kwargs)
