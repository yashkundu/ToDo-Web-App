from django.urls import path
from .views import UserDetailAPIView


app_name = 'api-users'


urlpatterns = [
    path('<slug:username>/', UserDetailAPIView.as_view())
]
