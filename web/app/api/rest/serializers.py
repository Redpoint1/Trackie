from rest_auth.serializers import TokenSerializer
from rest_auth.app_settings import DefaultUserDetailsSerializer


class TokenSerializer(TokenSerializer):
    """Extended TokenSerializer"""

    user = DefaultUserDetailsSerializer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = ('key', 'user',)
