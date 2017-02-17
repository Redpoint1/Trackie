from rest_framework.serializers import HyperlinkedModelSerializer
from ......trackie.models import Projection


class ProjectionSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Projection
        fields = "__all__"
