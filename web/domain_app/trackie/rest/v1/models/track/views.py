from rest_framework.viewsets import ModelViewSet
from .serializers import TrackSerializer
from ......trackie.models import Track


class TrackViewSet(ModelViewSet):
    serializer_class = TrackSerializer
    queryset = Track.objects.all()
    lookup_field = "slug"
    lookup_value_regex = "[-_\w]+"

    def list(self, request, *args, **kwargs):
        return super(TrackViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(TrackViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.request.data["owner"] = self.request.user.id

        return super(TrackViewSet, self).create(request, *args, **kwargs)
