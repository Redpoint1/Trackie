import rest_framework.views as rest_views
import rest_framework.response as rest_response


class TestEndpoint(rest_views.APIView):
    name = 'trackieApiTestEndpoint'

    def get(self, request, format=None):
        return rest_response.Response("test")
