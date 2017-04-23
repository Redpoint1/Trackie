from django.utils.translation import ugettext_lazy as _
from rest_framework.serializers import Serializer, SerializerMethodField
from rest_framework.exceptions import APIException
from ......trackie.models import Tournament, Track, Race, Racer
from ..tournament.serializers import TournamentSerializer
from ..track.serializers import TrackSerializer
from ..racer.serializers import RacerSerializer
from ..race.serializers import RaceSerializer

SERIALIZERS = {
    Tournament._meta.object_name: TournamentSerializer,
    Track._meta.object_name: TrackSerializer,
    Racer._meta.object_name: RacerSerializer,
    Race._meta.object_name: RaceSerializer,
}


class FullSearchSerializer(Serializer):

    def to_representation(self, obj):
        class_name = obj.__class__.__name__
        serializer = SERIALIZERS.get(class_name)
        if serializer is None:
            raise APIException(_("Unable to find serializer for {}").format(class_name))
        result = serializer(obj, context=self.context)
        return result.data
