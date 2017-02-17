from rest_framework.serializers import (HyperlinkedModelSerializer,
                                        SerializerMethodField)
from ......trackie.models import RacerInRace, Racer


class RaceRacerSerializer(HyperlinkedModelSerializer):
    number = SerializerMethodField("get_num")

    def get_num(self, instance):
        item = self.context["view"].queryset[0].race
        racer_rel = RacerInRace.objects.get(racer=instance, race=item)
        return racer_rel.number

    class Meta:
        model = Racer
        fields = "__all__"


class RacerSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Racer
        fields = "__all__"
