import rest_framework.views as restApiViews
import rest_framework.response as restApiResponse


class ApiRoot(restApiViews.APIView):

    name = "restV1_api"

    def get(self, request, format=None):

        return restApiResponse.Response("OK")

