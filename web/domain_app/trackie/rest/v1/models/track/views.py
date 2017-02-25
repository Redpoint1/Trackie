from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from .serializers import TrackSerializer
from ....permissions import IsOwnerOrReadOnly, IsNotPublicOrReadOnly
from ......trackie.models import Track


class TrackViewSet(ModelViewSet):
    serializer_class = TrackSerializer
    lookup_field = "slug"
    lookup_value_regex = "[-_\w]+"
    permission_classes = (IsOwnerOrReadOnly, IsNotPublicOrReadOnly,)

    def list(self, request, *args, **kwargs):
        return super(TrackViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super(TrackViewSet, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        return super(TrackViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(TrackViewSet, self).update(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            queryset = Track.objects.filter(public=True)
        else:
            queryset = Track.objects.filter(
                Q(public=True) | Q(owner=self.request.user)
            )
        return queryset
