from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from .models import Course, Lesson
from .permissions import IsModerator, IsOwner
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
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
