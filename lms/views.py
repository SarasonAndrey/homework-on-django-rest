import stripe
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Course, Lesson, Subscription
from .paginators import MyPagination
from .permissions import IsModerator, IsOwner
from .serializers import CourseSerializer, LessonSerializer
from .services import create_stripe_session


class CourseViewSet(viewsets.ModelViewSet):
    """
    Управление курсами.

    - GET /courses/ — список
    - POST /courses/ — создание (не модератор)
    - PUT/PATCH /courses/1/ — редактирование
    - DELETE /courses/1/ — удаление (только владелец)
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MyPagination
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, IsOwner]
        elif self.action == "retrieve":
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        else:  # list
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):

        if self.request.user.groups.filter(name="moderators").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = MyPagination
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, IsOwner]
        elif self.action == "retrieve":
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_subscription(request, course_id):
    """
    Подписаться или отписаться от курса
    Если подписка есть — удалит, если нет — создаст
    """
    course = get_object_or_404(Course, id=course_id)
    subscription, created = Subscription.objects.get_or_create(
        user=request.user, course=course
    )

    if created:
        return Response(
            {"message": "Подписка оформлена"}, status=status.HTTP_201_CREATED
        )

    subscription.delete()
    return Response({"message": "Подписка отменена"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_payment(request, course_id):
    """Создать сессию оплаты"""
    course = get_object_or_404(Course, id=course_id)
    result = create_stripe_session(course, request.user)
    return Response(result, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_payment_status(request, session_id):
    """Получить статус платежа из Stripe"""
    session = stripe.checkout.Session.retrieve(session_id)
    return Response({"status": session.payment_status})
