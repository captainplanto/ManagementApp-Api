
# Views for the userAPI.
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    # create new object in the database.
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    # Create new auth token for users.
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    # Manage the authenticated user.
    serializer_class = UserSerializer
    # Next two lines checks that user using the Api is authenticated to use this Api.
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Retrieve and return the authenticated user
        return self.request.user
