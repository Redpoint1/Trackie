import django.contrib.auth.models as auth_model
import rest_framework.serializers as serializers
import rest_framework.reverse as reverse
import domain_app.trackie.models as models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth_model.User
        fields = ("username", "first_name", "last_name")


class RaceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RaceType
        exclude = ("slug",)
        extra_kwargs = {
            "url": {
                "lookup_field": "slug",
            },
        }


class SportTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.SportType
        exclude = ("slug",)
        extra_kwargs = {
            "url": {
                "lookup_field": "slug",
            },
        }


class TournamentSerializer(serializers.HyperlinkedModelSerializer):
    # override relation
    races = serializers.SerializerMethodField("races_url")
    sport = SportTypeSerializer()

    def races_url(self, obj):
        kwargs = {
            "slug": obj.slug,
        }
        return reverse.reverse(
            "tournament-races-list",
            kwargs=kwargs,
            request=self.context.get("request")
        )

    class Meta:
        model = models.Tournament
        fields = ("name", "sport", "url", "races",)
        extra_kwargs = {
            "url": {
                "lookup_field": "slug",
            }
        }


class TrackSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = models.Track
        exclude = ("slug",)
        extra_kwargs = {
            "url": {
                "lookup_field": "slug",
            },
        }


class RaceSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    type = RaceTypeSerializer()
    track = TrackSerializer()
    tournament = TournamentSerializer()

    class Meta:
        model = models.Race
