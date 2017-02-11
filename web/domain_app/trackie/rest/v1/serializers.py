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
        fields = "__all__"
        extra_kwargs = {
            "url": {
                "lookup_field": "slug",
            },
        }


class SportTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.SportType
        fields = "__all__"

        extra_kwargs = {
            "url": {
                "lookup_field": "slug",
            },
        }


class TournamentSerializer(serializers.HyperlinkedModelSerializer):
    # override relation
    races = serializers.SerializerMethodField("races_url")
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

    class Meta:
        model = models.Tournament
        fields = "__all__"
        extra_kwargs = {
            "url": {
                "lookup_field": "slug",
            }
        }


class TrackSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = models.Track
        fields = "__all__"
        extra_kwargs = {
            "url": {
                "lookup_field": "slug",
            },
        }


class RacerInRaceSerializer(serializers.ModelSerializer):
    id = serializers.Field(source='group.id')
    number = serializers.Field(source='group.name')

    class Meta:
        model = models.RacerInRace
        exclude = ("racer", "race",)


class RacerSerializer(serializers.HyperlinkedModelSerializer):
    number = serializers.SerializerMethodField("get_num")

    def get_num(self, instance):
        item = self.context["view"].queryset[0].race
        racer_rel = models.RacerInRace.objects.get(racer=instance, race=item)
        return racer_rel.number

    class Meta:
        model = models.Racer
        fields = "__all__"


class ProjectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Projection
        fields = "__all__"


class RaceSerializer(serializers.HyperlinkedModelSerializer):
    type = RaceTypeSerializer()
    track = TrackSerializer()
    tournament = TournamentSerializer()
    data = serializers.SerializerMethodField("data_url")
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
        model = models.Race
        fields = "__all__"
