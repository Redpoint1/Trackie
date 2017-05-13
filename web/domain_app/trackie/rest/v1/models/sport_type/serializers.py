from ....serializers import OwnHyperlinkedModelSerializer
from ......trackie.models import SportType


class SportTypeSerializer(OwnHyperlinkedModelSerializer):
    class Meta:
        model = SportType
        fields = "__all__"

        extra_kwargs = {
            "url": {
                "lookup_field": "slug",
            },
        }
