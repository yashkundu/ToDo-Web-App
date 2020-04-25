from rest_framework.views import APIView
from .permissions import AnonPermissionOnly
from django.utils import timezone
import datetime

from rest_framework.response import Response
from django.contrib.auth import authenticate

from rest_framework import generics

from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model

from .serializers import UserRegisterSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()


class AuthAPIView(APIView):
    permission_classes = [AnonPermissionOnly]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'detail': 'You are already authenticated.'},status=400)
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        print(datetime.datetime.now())
        print(timezone.localtime(timezone.now()))
        if user is not None:
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            response = jwt_response_payload_handler(token, user, request=request)
            return Response(response)
        return Response({'detail':'Invalid credentials.'}, status=401)



class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AnonPermissionOnly]

    
