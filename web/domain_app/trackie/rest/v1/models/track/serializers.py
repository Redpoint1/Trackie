from django.contrib.auth.models import User
from rest_framework.serializers import HyperlinkedModelSerializer, Field
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
        presentation_serializer=UserSerializer,
        read_only=True
    )
    file = GPXFieldBase()

    class Meta:
        model = Track
        fields = ("id", "url", "name", "file", "public", "owner")
