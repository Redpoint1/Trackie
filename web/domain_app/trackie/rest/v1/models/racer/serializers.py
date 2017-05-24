from rest_framework.serializers import SerializerMethodField
from ....fields import ImageLimitField
from ....serializers import OwnHyperlinkedModelSerializer
from .....validators import FileSizeMaxValidator
from ......trackie.models import RacerInRace, Racer

# from django_countries.serializer_fields import CountryField


class ShortRacerSerialiter(OwnHyperlinkedModelSerializer):
    # country = CountryField()

    class Meta:
        model = Racer
        exclude = ("about", "photo")


class RacerSerializer(ShortRacerSerialiter):
    photo = ImageLimitField(
        sizes=[
            ('normal', 'url'),
            ('thumbnail', 'crop__150x200'),
        ],
        validators=[FileSizeMaxValidator(512*1024)],
        required=False,
        allow_null=True,
    )

    class Meta(ShortRacerSerialiter.Meta):
        exclude = ()


class RaceRacerSerializer(RacerSerializer):
    number = SerializerMethodField("get_num")

    def get_num(self, instance):
        item = self.context["view"].queryset[0].race
        racer_rel = RacerInRace.objects.get(racer=instance, race=item)
        return racer_rel.number

    class Meta(RacerSerializer.Meta):
        fields = ("id", "url", "first_name", "last_name", "photo", "number",)
