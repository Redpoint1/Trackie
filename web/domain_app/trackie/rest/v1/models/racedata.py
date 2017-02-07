from django.utils.timezone import datetime
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
# from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.serializers import HyperlinkedRelatedField, RelatedField
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from ....models import RaceData, Race, Racer
from ..serializers import RaceSerializer, RacerSerializer


# class RaceDataPaginator(LimitOffsetPagination):
#     default_limit = 50
#     max_limit = 100


class RaceDataGeoJSONPostSerializer(GeoFeatureModelSerializer):
    race = HyperlinkedRelatedField("race-detail", queryset=Race.objects.all())

    class Meta:
        model = RaceData
        geo_field = "position"
        exclude = []


class RaceDataGeoJSONSerializer(RaceDataGeoJSONPostSerializer):
    race = HyperlinkedRelatedField("race-detail", read_only=True)
    racer = RacerSerializer()


class RaceDataViewSet(viewsets.ModelViewSet):
    # pagination_class = RaceDataPaginator
    queryset = Race.objects.all()

    def list(self, request, *args, **kwargs):
        self.serializer_class = RaceDataGeoJSONSerializer
        last = Race.objects.get(pk=kwargs["race_pk"]).data.last()
        self.queryset = Race.objects.get(pk=kwargs["race_pk"]).data.filter(received=last.received)
        return super(RaceDataViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        bulk = isinstance(request.data, list)
        self.serializer_class = RaceDataGeoJSONPostSerializer
        race = Race.objects.get(pk=kwargs["race_pk"])
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

    def destroy(self, request, *args, **kwargs):
        race = Race.objects.get(pk=kwargs["race_pk"])
        race.end = datetime.now()
        race.save()
        return Response(status=status.HTTP_200_OK)

