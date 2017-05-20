from rest_framework.viewsets import ModelViewSet
from .serializers import ProjectionSerializer
from ......trackie.models import Projection
from ....permissions import ReadOnly


class ProjectionViewSet(ModelViewSet):
    queryset = Projection.objects.all()
    serializer_class = ProjectionSerializer
    permission_classes = (ReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        """ Projection detail """
        return super(ProjectionViewSet, self).retrieve(
            request,
            *args,
            **kwargs
        )
