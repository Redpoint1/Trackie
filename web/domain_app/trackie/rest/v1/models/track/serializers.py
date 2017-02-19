from django.contrib.auth.models import User
from rest_framework.serializers import HyperlinkedModelSerializer
from drf_extra_fields.fields import Base64FileField
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from ..user.serializers import UserSerializer
from ......trackie.models import Track
import xml.etree.ElementTree as ET

class GPXFieldBase(Base64FileField):
    ALLOWED_TYPES = ['gpx']

    def get_file_extension(self, filename, decoded_file):
        tag = ET.ElementTree(ET.fromstring(decoded_file)).getroot().tag
        if "gpx" in tag:
            return 'gpx'
        return None


class TrackSerializer(HyperlinkedModelSerializer):
    owner = PresentablePrimaryKeyRelatedField(
        queryset=User.objects,
        presentation_serializer=UserSerializer
    )
    file = GPXFieldBase(required=True)

    class Meta:
        model = Track
        fields = "__all__"
        extra_kwargs = {
            "url": {
                "lookup_field": "slug",
            },
        }