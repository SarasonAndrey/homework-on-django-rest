from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from lms.views import CourseViewSet, LessonViewSet
from .views import api_root

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"lessons", LessonViewSet, basename="lesson")


schema_view = get_schema_view(
    openapi.Info(
        title="LMS API",
        default_version="v1",
        description="API для платформы обучения",
        contact=openapi.Contact(email="support@lms.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", api_root, name="api-root"),
    path(
        "api/",
        include(
            [
                path("", include(router.urls)),  # /api/courses/
                path("users/", include("users.urls")),  # /api/users/register/
                path("lms/", include("lms.urls")),  # /api/lms/lessons/
            ]
        ),
    ),
    re_path(r"^swagger/$", schema_view.with_ui("swagger"), name="schema-swagger-ui"),
    re_path(r"^redoc/$", schema_view.with_ui("redoc"), name="schema-redoc"),
]
