from django.urls import path
from .views import (
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonCreateAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView
)

urlpatterns = [
    path('', LessonListAPIView.as_view(), name='lesson-list'),
    path('<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'),
    path('create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
]