""" Rest api views v1 for domain """

import rest_framework.views as rest_views
import rest_framework.response as rest_response


class TestEndpoint(rest_views.APIView):
    """ Temporary endpoint """
    name = 'trackieApiTestEndpoint'

    def get(self, request, format=None):
        """

        :param request:
        :param format:
        :return:
        """
        return rest_response.Response("test")
