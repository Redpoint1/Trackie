from rest_framework.serializers import (HyperlinkedModelSerializer,
                                        SerializerMethodField)
from drf_extra_fields.fields import Base64ImageField
from ......trackie.models import RacerInRace, Racer


class RacerSerializer(HyperlinkedModelSerializer):
    photo = Base64ImageField(required=False)

    class Meta:
        model = Racer
        fields = "__all__"


class RaceRacerSerializer(RacerSerializer):
    number = SerializerMethodField("get_num")

    def get_num(self, instance):
        item = self.context["view"].queryset[0].race
        racer_rel = RacerInRace.objects.get(racer=instance, race=item)
        return racer_rel.number

    class Meta(RacerSerializer.Meta):
        pass
