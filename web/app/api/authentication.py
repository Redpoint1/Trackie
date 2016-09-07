from rest_framework.authentication import BasicAuthentication


class ExtendedBasicAuthentication(BasicAuthentication):
    """Extended class of the BasicAuthentication to avoid to show the
    authentication dialog in the browser"""

    def authenticate_header(self, request):
        return 'X-Basic realm="%s"' % self.www_authenticate_realm
