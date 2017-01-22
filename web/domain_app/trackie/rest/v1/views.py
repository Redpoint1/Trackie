""" Rest api views v1 for domain """

import rest_framework.generics as views
import domain_app.trackie.rest.v1.serializers as serializers
import domain_app.trackie.models as models


class RacesEndpoint(views.ListAPIView):
    """ List of all races """
    name = 'race-list'
    serializer_class = serializers.RaceSerializer
    queryset = models.Race.objects.all()


class RaceEndpoint(views.RetrieveAPIView):
    """ Race detail """
    name = 'race-detail'
    serializer_class = serializers.RaceSerializer
    queryset = models.Race.objects.all()


class SportTypesEndpoint(views.ListAPIView):
    """ Sport type list """
    name = 'sporttype-list'
    serializer_class = serializers.SportTypeSerializer
    queryset = models.SportType.objects.all()


class SportTypeEndpoint(views.RetrieveAPIView):
    """ Sport type detail """
    name = 'sporttype-detail'
    serializer_class = serializers.SportTypeSerializer
    queryset = models.SportType.objects.all()
    lookup_field = "slug"
    lookup_url_kwarg = "slug"

class RaceTypesEndpoint(views.ListAPIView):
    """ Race type list """
    name = 'racetype-list'
    serializer_class = serializers.RaceTypeSerializer
    queryset = models.RaceType.objects.all()


class RaceTypeEndpoint(views.RetrieveAPIView):
    """ Race type detail """
    name = 'racetype-detail'
    serializer_class = serializers.RaceTypeSerializer
    queryset = models.RaceType.objects.all()
    lookup_field = "slug"
    lookup_url_kwarg = "slug"


class TracksEndpoint(views.ListAPIView):
    """ Track list """
    name = 'track-list'
    serializer_class = serializers.TrackSerializer
    queryset = models.Track.objects.all()


class TrackEndpoint(views.RetrieveAPIView):
    """ Track detail """
    name = 'track-detail'
    serializer_class = serializers.TrackSerializer
    queryset = models.Track.objects.all()
    lookup_field = "slug"
    lookup_url_kwarg = "slug"


class TournamentsEndpoint(views.ListAPIView):
    """ Tournament list """
    name = 'tournament-list'
    serializer_class = serializers.TournamentSerializer
    queryset = models.Tournament.objects.all()


class TournamentEndpoint(views.RetrieveAPIView):
    """ Tournament detail """
    name = 'tournament-detail'
    serializer_class = serializers.TournamentSerializer
    queryset = models.Tournament.objects.all()
    lookup_field = "slug"
    lookup_url_kwarg = "slug"


class TournamentRacesEndpoint(views.ListAPIView):
    """ Tournament detail """
    name = 'tournament-races-list'
    serializer_class = serializers.RaceSerializer

    def get_queryset(self):
        # models.Race.objects.filter(tournament__slug=self.kwargs.get("slug"))
        return models.Tournament.objects.get(**self.kwargs).races.all()


