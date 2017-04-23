from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import FullSearchSerializer
from .....models import Tournament, Track, Race, Racer


class SearchViewSet(ReadOnlyModelViewSet):
    serializer_class = FullSearchSerializer

    def get_queryset(self):
        query = self.request.query_params.get("q")
        if query is None:
            raise ParseError(_("Missing search parameter"))
        query = query.strip()
        if len(query) < 3:
            raise ParseError(_("Search string must be at least 3 characters long"))

        all_results = {
            Tournament._meta.model_name: Tournament.objects.filter(name__unaccent__icontains=query),
            Track._meta.model_name: Track.objects.filter(name__unaccent__icontains=query, public=True),
            Race._meta.model_name: Race.objects.filter(name__unaccent__icontains=query),
            Racer._meta.model_name: Racer.objects.filter(full_name__unaccent__icontains=query),
        }
        return all_results

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        for class_name, query in queryset.items():
            serializer = self.get_serializer(query, many=True)
            queryset[class_name] = serializer.data

        return Response(queryset)
