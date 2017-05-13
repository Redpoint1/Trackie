from rest_framework.serializers import SerializerMethodField
import rest_framework.reverse as reverse
from ..race_type.serializers import RaceTypeSerializer
from ..track.serializers import TrackSerializer
from ..tournament.serializers import TournamentSerializer
from ..projection.serializers import ProjectionSerializer
from ....serializers import OwnHyperlinkedModelSerializer
from ......trackie.models import Race


class ShortRaceSerializer(OwnHyperlinkedModelSerializer):

    tournament = TournamentSerializer()

    class Meta:
        model = Race
        fields = ("id", "url", "name", "tournament", "start", "end", "real_start", "real_end", "estimated_duration")


class RaceSerializer(ShortRaceSerializer):
    type = RaceTypeSerializer()
    track = TrackSerializer()
    data = SerializerMethodField("data_url")
    projection = ProjectionSerializer()
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
