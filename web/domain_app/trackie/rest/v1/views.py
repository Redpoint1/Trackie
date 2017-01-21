""" Rest api views v1 for domain """

import rest_framework.generics as views
import domain_app.trackie.rest.v1.serializers as serializers
import domain_app.trackie.models as models


class RacesEndpoint(views.ListAPIView):
    """ List of all races """
    name = 'race-list'
    serializer_class = serializers.RaceSerializer
    queryset = models.Race.objects.all()


class RaceEndpoint(RacesEndpoint):
    """ Race detail """
    name = 'race-detail'


class RaceTypesEndpoint(views.ListAPIView):
    """ Race type list """
    name = 'racetype-list'
    serializer_class = serializers.RaceTypeSerializer
    queryset = models.RaceType.objects.all()


class RaceTypeEndpoint(RaceTypesEndpoint):
    """ Race type detail """
    name = 'racetype-detail'
    lookup_field = "slug"
    lookup_url_kwarg = "slug"


class TracksEndpoint(views.ListAPIView):
    """ Track list """
    name = 'track-list'
    serializer_class = serializers.TrackSerializer
    queryset = models.Track.objects.all()


class TrackEndpoint(TracksEndpoint):
    """ Track detail """
    name = 'track-detail'
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
