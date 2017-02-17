from rest_framework.serializers import HyperlinkedRelatedField
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from ..racer.serializers import RaceRacerSerializer
from ......trackie.models import RaceData, Race


class RaceDataGeoJSONPostSerializer(GeoFeatureModelSerializer):
    race = HyperlinkedRelatedField("race-detail", queryset=Race.objects.all())

    class Meta:
        model = RaceData
        geo_field = "position"
        exclude = []


class RaceDataGeoJSONSerializer(RaceDataGeoJSONPostSerializer):
    race = HyperlinkedRelatedField("race-detail", read_only=True)
    racer = RaceRacerSerializer()
