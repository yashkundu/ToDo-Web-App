import datetime

from rest_framework_jwt.settings import api_settings

expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'username': user.username,
        'expires': datetime.datetime.now() + expire_delta - datetime.timedelta(seconds=60)
    }
