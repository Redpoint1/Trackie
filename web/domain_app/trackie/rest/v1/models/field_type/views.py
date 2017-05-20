from rest_framework.viewsets import ModelViewSet
from .serializers import FieldTypeSerializer
from ......trackie.models import FieldType
from ....permissions import ReadOnly


class FieldTypeViewSet(ModelViewSet):
    queryset = FieldType.objects.all()
    serializer_class = FieldTypeSerializer
    permission_classes = (ReadOnly,)
