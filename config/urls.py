from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from lms.views import CourseViewSet
from .views import api_root

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")

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
    path("api/", include("lms.urls")),
    path("", api_root, name="api-root"),
    path(
        "api/",
        include(
            [
                path("", include(router.urls)),
                path("users/", include("users.urls")),
                path("lms/", include("lms.urls")),
            ]
        ),
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
