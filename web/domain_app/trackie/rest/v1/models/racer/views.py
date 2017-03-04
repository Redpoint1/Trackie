from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import RacerSerializer
from ......trackie.models import Racer


class RacerViewSet(ModelViewSet):
    serializer_class = RacerSerializer
    queryset = Racer.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request, *args, **kwargs):
        return super(RacerViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super(RacerViewSet, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(RacerViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(RacerViewSet, self).update(request, *args, **kwargs)
