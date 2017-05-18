# from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class AuthTokenView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = None
    name = "trackie_apikey"

    def get(self, request, *args, **kwargs):
        return Response({'token': request.user.auth_token.key})
