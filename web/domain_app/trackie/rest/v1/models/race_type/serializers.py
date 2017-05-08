from rest_framework.serializers import HyperlinkedModelSerializer
from ..field_type.serializers import FieldTypeSerializer
from ......trackie.models import RaceType


class RaceTypeSerializer(HyperlinkedModelSerializer):

    fields = FieldTypeSerializer(many=True)

    class Meta:
        model = RaceType
        exclude = ("owner",)
