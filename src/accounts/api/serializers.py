import datetime

from rest_framework import serializers
from django.contrib.auth import get_user_model

from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA

User = get_user_model()



class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username'
        ]



class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    expires = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
            'token',
            'expires'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def get_token(self, obj):
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def get_expires(self, obj):
        return datetime.datetime.now() + expire_delta - datetime.timedelta(seconds=60)

    def validate_username(self, value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError('User with this username already exists.')
        return value

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError('User with this email already exists.')
        return value

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError('Passwords must match.')
        return data

    def create(self, validated_data):
        user_obj = User(
            username = validated_data.get('username'),
            email = validated_data.get('email')
        )
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()
        return user_obj
