from rest_framework.viewsets import ModelViewSet
from .serializers import ProjectionSerializer
from ......trackie.models import Projection


class ProjectionViewSet(ModelViewSet):
    queryset = Projection.objects.all()
    serializer_class = ProjectionSerializer

    def retrieve(self, request, *args, **kwargs):
        """ Projection detail """
        return super(ProjectionViewSet, self).retrieve(
            request,
            *args,
            **kwargs
        )