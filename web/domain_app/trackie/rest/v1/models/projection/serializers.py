from ....serializers import OwnHyperlinkedModelSerializer
from ......trackie.models import Projection


class ProjectionSerializer(OwnHyperlinkedModelSerializer):
    class Meta:
        model = Projection
        fields = "__all__"
