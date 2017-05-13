from ....serializers import OwnHyperlinkedModelSerializer
from ..field_type.serializers import FieldTypeSerializer
from ......trackie.models import RaceType


class RaceTypeSerializer(OwnHyperlinkedModelSerializer):

    fields = FieldTypeSerializer(many=True)

    class Meta:
        model = RaceType
        exclude = ("owner",)
