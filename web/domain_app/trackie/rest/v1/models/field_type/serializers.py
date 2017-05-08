from rest_framework.serializers import ModelSerializer
from ......trackie.models import FieldType


class FieldTypeSerializer(ModelSerializer):
    class Meta:
        model = FieldType
        fields = "__all__"
