""" Rest api views V1 """

import rest_framework.views as rest_views
import rest_framework.response as rest_response


class ApiRoot(rest_views.APIView):
    """
    Api root for rest
    """
    name = "restV1_api"

    def get(self, request, format=None):
        """

        :param request:
        :param format:
        :return:
        """
        return rest_response.Response("OK")
