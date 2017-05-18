from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from rest_framework_bulk import BulkSerializerMixin
from rest_framework.serializers import ModelSerializer
from ..racer.serializers import ShortRacerSerialiter
from ......trackie.models import RacerInRace, Racer
from ....serializers import FixBulkListSerializer


class ParticipantsSerializer(BulkSerializerMixin, ModelSerializer):

    racer = PresentablePrimaryKeyRelatedField(
        presentation_serializer=ShortRacerSerialiter,
        queryset=Racer.objects.all(),
        required=True,
    )

    class Meta:
        model = RacerInRace
        fields = "__all__"
        list_serializer_class = FixBulkListSerializer