from rest_framework.serializers import (HyperlinkedModelSerializer,
                                        SerializerMethodField)
import rest_framework.reverse as reverse
from ..sport_type.serializers import SportTypeSerializer
from ..user.serializers import UserSerializer
from ......trackie.models import Tournament


class ShortTournamentSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Tournament
        fields = ("url", "name", "slug")
        extra_kwargs = {
            "url": {
                "lookup_field": "slug",
            }
        }


class TournamentSerializer(ShortTournamentSerializer):
    # override relation
    races = SerializerMethodField("races_url")
    sport = SportTypeSerializer()
    owner = UserSerializer()

    def races_url(self, obj):
        kwargs = {
            "slug": obj.slug,
        }
        return reverse.reverse(
            "tournament-races-list",
            kwargs=kwargs,
            request=self.context.get("request")
        )

    class Meta(ShortTournamentSerializer.Meta):
        fields = "__all__"
