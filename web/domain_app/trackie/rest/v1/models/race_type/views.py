from rest_framework.viewsets import ModelViewSet
from .serializers import RaceTypeSerializer
from ......trackie.models import RaceType


class RaceTypeViewSet(ModelViewSet):
    serializer_class = RaceTypeSerializer
    queryset = RaceType.objects.all()
    lookup_field = "slug"
    lookup_value_regex = "[-_\w]+"

    def list(self, request, *args, **kwargs):
        return super(RaceTypeViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(RaceTypeViewSet, self).retrieve(request, *args, **kwargs)
