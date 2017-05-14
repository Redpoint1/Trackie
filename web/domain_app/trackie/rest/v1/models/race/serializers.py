from rest_framework.serializers import SerializerMethodField
import rest_framework.reverse as reverse
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from ..race_type.serializers import RaceTypeSerializer
from ..track.serializers import TrackSerializer
from ..tournament.serializers import TournamentSerializer
from ..projection.serializers import ProjectionSerializer
from ....serializers import OwnHyperlinkedModelSerializer
from ......trackie.models import Race, Tournament, RaceType, Track, Projection


class ShortRaceSerializer(OwnHyperlinkedModelSerializer):

    tournament = PresentablePrimaryKeyRelatedField(
        presentation_serializer=TournamentSerializer,
        queryset=Tournament.objects.all(),
    )

    class Meta:
        model = Race
        fields = ("id", "url", "name", "tournament", "start", "end", "real_start", "real_end", "estimated_duration")


class RaceSerializer(ShortRaceSerializer):
    type = PresentablePrimaryKeyRelatedField(
        presentation_serializer=RaceTypeSerializer,
        queryset=RaceType.objects.all(),
    )
    track = PresentablePrimaryKeyRelatedField(
        presentation_serializer=TrackSerializer,
        queryset=Track.objects.all(),
    )
    projection = PresentablePrimaryKeyRelatedField(
        presentation_serializer=ProjectionSerializer,
        queryset=Projection.objects.all(),
        required=False,
        allow_null=True,
    )

    data = SerializerMethodField("data_url")
    records_count = SerializerMethodField("count")

    def count(self, obj):
        return obj.data.datetimes("received", "second").count()

    def data_url(self, obj):
        kwargs = {
            "race_pk": obj.pk,
        }
        return reverse.reverse(
            "racedata-list",
            kwargs=kwargs,
            request=self.context.get("request")
        )

    class Meta:
        model = Race
        fields = "__all__"
