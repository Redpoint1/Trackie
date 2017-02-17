from rest_framework.viewsets import ModelViewSet
from .serializers import SportTypeSerializer
from ......trackie.models import SportType


class SportTypeViewSet(ModelViewSet):
    serializer_class = SportTypeSerializer
    queryset = SportType.objects.all()
    lookup_field = "slug"
    lookup_value_regex = "[-_\w]+"

    def list(self, request, *args, **kwargs):
        return super(SportTypeViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(SportTypeViewSet, self).retrieve(request, *args, **kwargs)
