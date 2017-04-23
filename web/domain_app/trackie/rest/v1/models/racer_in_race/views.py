from rest_framework.viewsets import ReadOnlyModelViewSet
from ..race.serializers import ShortRaceSerializer
from ......trackie.models import Race


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
