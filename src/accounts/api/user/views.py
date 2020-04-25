from rest_framework import generics, permissions
from accounts.api.permissions import IsUserPresent
from django.contrib.auth import get_user_model
from .serializers import UserDetailSerializer


User = get_user_model()

class UserDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsUserPresent]
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'username'

    def get_serializer_context(self):
        return {'request': self.request}
