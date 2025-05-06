from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.user.serializers import profille as serializers
from apps.user import models


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.ProfileSerializerForGet
    permission_classes = (IsAuthenticated, )
    http_method_names = ('patch', 'get')

    def get_object(self):
        return self.request.user