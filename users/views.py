from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from lms.models import Course
from lms.services import create_stripe_session
from .models import Payment, User
from .permissions import IsOwnerOrAdmin
from .serializers import (
    MyTokenObtainPairSerializer,
    PaymentSerializer,
    UserRegisterSerializer,
    UserSerializer,
)

User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Или [IsAdminUser], если нужно


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin]


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin]


class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def perform_destroy(self, instance):
        if instance.is_superuser:
            raise PermissionDenied("Нельзя удалить суперпользователя.")
        instance.delete()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderators").exists() or user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=user)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_payment(request, course_id):
    """Создать сессию оплаты курса"""
    course = get_object_or_404(Course, id=course_id)
    result = create_stripe_session(course, request.user)
    return Response(result, status=status.HTTP_201_CREATED)
