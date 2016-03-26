import rest_framework.views as rest_views
import rest_framework.response as rest_response


class ApiRoot(rest_views.APIView):
    name = "restV1_api"

    def get(self, request, format=None):
        return rest_response.Response("OK")
