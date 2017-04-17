from django.utils.timezone import datetime, timedelta
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets, status, exceptions
from rest_framework.exceptions import ValidationError
# from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from .serializers import (RaceDataGeoJSONPostSerializer,
                          RaceDataGeoJSONSerializer)
from ..race.serializers import RaceSerializer
from ......trackie.models import Race, RaceData


# class RaceDataPaginator(LimitOffsetPagination):
#     default_limit = 50
#     max_limit = 100


class RaceFinishedException(exceptions.APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _("The race has already been ended.")
    default_code = 'forbidden'


class RaceDataViewSet(viewsets.ModelViewSet):
    # pagination_class = RaceDataPaginator
    queryset = Race.objects.all()

    def list(self, request, *args, **kwargs):
        self.serializer_class = RaceDataGeoJSONSerializer
        race = Race.objects.get(pk=kwargs["race_pk"])
        if race.end:
            return Response(status=status.HTTP_204_NO_CONTENT)
        last = race.data.last()
        self.queryset = Race.objects.get(pk=kwargs["race_pk"]).data
        if last:
            self.queryset = self.queryset.filter(received=last.received)
        return super(RaceDataViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        bulk = isinstance(request.data, list)
        self.serializer_class = RaceDataGeoJSONPostSerializer
        race = Race.objects.get(pk=kwargs["race_pk"])
        if not race.data.count():
            race.real_start = datetime.now()
            race.save()
        if race.end:
            raise RaceFinishedException
        racers = race.racers.all().values("number", "racer")
        # dict(racer.number: racer.id)
        racers = dict([(racer["number"], racer["racer"]) for racer in racers])
        url = RaceSerializer(race, context={'request': request}).data["url"]
        now = datetime.now()

        if bulk:
            errors = []
            for obj in request.data:
                obj["race"] = url
                obj["received"] = now
                try:
                    obj["racer"] = racers[obj["racer"]]
                except KeyError:
                    errors.append({
                        "racer": _(
                            "Racer with number {} doesn't exist"
                        ).format(obj["racer"])
                    })
                else:
                    errors.append({})
            if any(errors):
                raise ValidationError(detail=errors)
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
        else:
            request.data["race"] = url
            request.data["received"] = now
            try:
                request.data["racer"] = racers[request.data["racer"]]
            except KeyError:
                raise ValidationError(detail={"racer": _(
                            "Racer with number {} doesn't exist"
                        ).format(request.data["racer"])})
            return super(RaceDataViewSet, self).create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        race = Race.objects.get(pk=kwargs["race_pk"])
        race.end = datetime.now()
        race.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RaceDataReplayViewSet(viewsets.ModelViewSet):
    # pagination_class = RaceDataPaginator
    queryset = Race.objects.all()

    def list(self, request, *args, **kwargs):
        self.serializer_class = RaceDataGeoJSONSerializer

        from_seconds = int(request.query_params.get("from", 0))
        count = int(request.query_params.get("count", 10))

        from_time = datetime.fromtimestamp(from_seconds)

        time_ranges = RaceData.objects.filter(
            received__gt=from_time,
            race=kwargs["race_pk"]
        ).order_by("received").datetimes("received", "second")[:count]

        result = []
        for time_range in time_ranges:
            time_range_max = time_range + timedelta(
                microseconds=timedelta.max.microseconds
            )

            self.queryset = RaceData.objects.filter(
                race=kwargs["race_pk"],
                received__range=(
                    time_range,
                    time_range_max
                )
            ).order_by("received", "racer_id")

            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            result.append(serializer.data)
        return Response(result)
