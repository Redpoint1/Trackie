from rest_framework.serializers import (SerializerMethodField,
                                        CurrentUserDefault)
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
import rest_framework.reverse as reverse
from ..sport_type.serializers import SportTypeSerializer
from ..user.serializers import UserSerializer
from ....serializers import OwnHyperlinkedModelSerializer
from ......trackie.models import Tournament, SportType


class ShortTournamentSerializer(OwnHyperlinkedModelSerializer):
    class Meta:
        model = Tournament
        fields = ("id", "url", "name")


class TournamentSerializer(ShortTournamentSerializer):
    # override relation
    races = SerializerMethodField("races_url")
    sport = PresentablePrimaryKeyRelatedField(
        queryset=SportType.objects.all(),
        presentation_serializer=SportTypeSerializer,
    )

    owner = PresentablePrimaryKeyRelatedField(
        presentation_serializer=UserSerializer,
        read_only=True,
        default=CurrentUserDefault()
    )

    def races_url(self, obj):
        kwargs = {
            "id": obj.id,
        }
        return reverse.reverse(
            "tournament-races-list",
            kwargs=kwargs,
            request=self.context.get("request")
        )

    class Meta(ShortTournamentSerializer.Meta):
        fields = "__all__"
