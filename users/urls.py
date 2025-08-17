from django.urls import path
from .views import PaymentListAPIView, UserRegisterView, MyTokenObtainPairView

app_name = "users"

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
]
