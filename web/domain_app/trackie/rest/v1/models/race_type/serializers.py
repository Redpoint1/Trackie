from rest_framework.fields import BooleanField, CurrentUserDefault, SerializerMethodField
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from ....serializers import OwnHyperlinkedModelSerializer
from ..field_type.serializers import FieldTypeSerializer
from ......trackie.models import RaceType, FieldType
from ..user.serializers import UserSerializer


class RaceTypeSerializer(OwnHyperlinkedModelSerializer):

    fields = PresentablePrimaryKeyRelatedField(
        required=True,
        presentation_serializer=FieldTypeSerializer,
        queryset=FieldType.objects.all(),
        many=True
    )

    public = BooleanField(
        read_only=True,
        default=False
    )

    owner = PresentablePrimaryKeyRelatedField(
        presentation_serializer=UserSerializer,
        read_only=True,
        default=CurrentUserDefault()
    )

    used = SerializerMethodField("is_used")

    def is_used(self, obj):
        return bool(obj.races.count())

    class Meta:
        model = RaceType
        fields = "__all__"
