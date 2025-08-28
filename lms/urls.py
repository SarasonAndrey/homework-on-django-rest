from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, subscribe_to_course, unsubscribe_from_course

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"lessons", LessonViewSet, basename="lesson")

urlpatterns = [
    path("", include(router.urls)),
    path('courses/<int:course_id>/subscribe/', subscribe_to_course, name='subscribe'),
    path('courses/<int:course_id>/unsubscribe/', unsubscribe_from_course, name='unsubscribe'),
]
