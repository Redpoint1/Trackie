from rest_framework.serializers import ModelSerializer, Field
from ......trackie.models import RacerInRace


class RacerInRaceSerializer(ModelSerializer):
    id = Field(source='group.id')
    number = Field(source='group.name')

    class Meta:
        model = RacerInRace
        exclude = ("racer", "race",)
