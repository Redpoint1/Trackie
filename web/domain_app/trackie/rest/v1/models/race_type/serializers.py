from rest_framework.serializers import HyperlinkedModelSerializer
from ......trackie.models import RaceType


class RaceTypeSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = RaceType
        fields = "__all__"
        extra_kwargs = {
            "url": {
                "lookup_field": "slug",
            },
        }


