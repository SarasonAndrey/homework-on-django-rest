from django.urls import path
from .views import (
    UserRegisterView,
    MyTokenObtainPairView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserDeleteAPIView,
)

app_name = "users"

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserRetrieveAPIView.as_view(), name="user-detail"),
    path("users/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", UserDeleteAPIView.as_view(), name="user-delete"),
]
