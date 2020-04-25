from django.urls import path

from .views import AuthAPIView, RegisterAPIView

app_name = 'api-accounts'

urlpatterns = [
    path('login/', AuthAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),
]
