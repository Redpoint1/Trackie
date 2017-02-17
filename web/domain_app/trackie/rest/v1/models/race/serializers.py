from rest_framework.serializers import (HyperlinkedModelSerializer,
                                        SerializerMethodField)
import rest_framework.reverse as reverse
from ..race_type.serializers import RaceTypeSerializer
from ..track.serializers import TrackSerializer
from ..tournament.serializers import TournamentSerializer
from ..projection.serializers import ProjectionSerializer
from ......trackie.models import Race


class RaceSerializer(HyperlinkedModelSerializer):
    type = RaceTypeSerializer()
    track = TrackSerializer()
    tournament = TournamentSerializer()
    data = SerializerMethodField("data_url")
    projection = ProjectionSerializer()

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
