from django.db.models import Q
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import TrackSerializer, UpdateTrackSerializer
from ....permissions import IsOwnerOrReadOnly, NotProtectedOrReadOnly
from ......trackie.models import Track


class TrackViewSet(ModelViewSet):
    serializer_class = TrackSerializer
    permission_classes = (IsOwnerOrReadOnly, NotProtectedOrReadOnly)
    trackie_protect = "races"

    def list(self, request, *args, **kwargs):
        return super(TrackViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super(TrackViewSet, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(TrackViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(TrackViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(TrackViewSet, self).destroy(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            queryset = Track.objects.filter(public=True)
        else:
            queryset = Track.objects.filter(
                Q(public=True) | Q(owner=self.request.user)
            )
        return queryset

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UpdateTrackSerializer
        else:
            return super(TrackViewSet, self).get_serializer_class()


class OwnTrackViewSet(ReadOnlyModelViewSet):
    serializer_class = TrackSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Track.objects.filter(owner=self.request.user)
