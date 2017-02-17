from rest_framework.serializers import HyperlinkedModelSerializer
from ......trackie.models import SportType


class SportTypeSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = SportType
        fields = "__all__"

        extra_kwargs = {
            "url": {
                "lookup_field": "slug",
            },
        }
