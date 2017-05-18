from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import ParseError
import rest_framework.mixins as mixins
from ..race.serializers import ShortRaceSerializer
from .serializers import ParticipantsSerializer
from ......trackie.models import Race, RacerInRace
from rest_framework_bulk.mixins import BulkCreateModelMixin, BulkUpdateModelMixin, BulkDestroyModelMixin


class RacerFinishedRace(ReadOnlyModelViewSet):
    serializer_class = ShortRaceSerializer

    def get_queryset(self):
        racer_id = self.kwargs.get("racer_id")
        self.queryset = Race.objects.filter(real_end__isnull=False, real_start__isnull=False, racers__racer_id=racer_id)
        return super(RacerFinishedRace, self).get_queryset()

    def list(self, request, *args, **kwargs):
        return super(RacerFinishedRace, self).list(request, *args, **kwargs)


class RacerRacingRace(ReadOnlyModelViewSet):
    serializer_class = ShortRaceSerializer

    def get_queryset(self):
        racer_id = self.kwargs.get("racer_id")
        self.queryset = Race.objects.filter(real_end__isnull=True, real_start__isnull=False, racers__racer_id=racer_id)
        return super(RacerRacingRace, self).get_queryset()

    def list(self, request, *args, **kwargs):
        return super(RacerRacingRace, self).list(request, *args, **kwargs)


class RacerUpcomingRace(ReadOnlyModelViewSet):
    serializer_class = ShortRaceSerializer

    def get_queryset(self):
        racer_id = self.kwargs.get("racer_id")
        self.queryset = Race.objects.filter(real_end__isnull=True, real_start__isnull=True, racers__racer_id=racer_id)
        return super(RacerUpcomingRace, self).get_queryset()

    def list(self, request, *args, **kwargs):
        return super(RacerUpcomingRace, self).list(request, *args, **kwargs)


class ParticipantsRaceView(
    BulkCreateModelMixin,
    BulkUpdateModelMixin,
    BulkDestroyModelMixin,
    mixins.ListModelMixin,
    GenericAPIView
):
    serializer_class = ParticipantsSerializer
    t_lookup_field = "race_id"
    t_lookup_url_kwarg = "pk"
    name = "raceparticipanrs"

    def get_queryset(self):
        return RacerInRace.objects.filter(**{self.t_lookup_field: self.kwargs.get(self.t_lookup_url_kwarg)})

    def get(self, request, *args, **kwargs):
        race = get_object_or_404(Race, pk=self.kwargs.get(self.t_lookup_url_kwarg))
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        race = get_object_or_404(Race, pk=self.kwargs.get(self.t_lookup_url_kwarg))
        bulk = isinstance(request.data, list)

        race.participants.clear()

        if bulk:
            for obj in request.data:
                obj["race"] = race.pk
        else:
            request.data["race"] = race.pk

        return super(ParticipantsRaceView, self).create(request, *args, **kwargs)
