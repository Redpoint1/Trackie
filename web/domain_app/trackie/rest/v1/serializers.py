import rest_framework.serializers as serializers
import domain_app.trackie.models as models


class RaceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RaceType
        exclude = ("slug",)
        extra_kwargs = {
            "url": {
                "lookup_field": "slug",
            },
        }


class TrackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Track
        exclude = ("slug", "owner",)
        extra_kwargs = {
            "url": {
                "lookup_field": "slug",
            },
        }


class RaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Race
        fields = ("pk", "name", "type", "track", "url")

    type = RaceTypeSerializer()
    track = TrackSerializer()
