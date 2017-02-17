from rest_framework.serializers import HyperlinkedModelSerializer
from ..user.serializers import UserSerializer
from ......trackie.models import Track


class TrackSerializer(HyperlinkedModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Track
        fields = "__all__"
        extra_kwargs = {
            "url": {
                "lookup_field": "slug",
            },
        }
