from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lms.views import CourseViewSet
from .views import api_root

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/lessons/", include("lms.urls")),
    path("", api_root, name="api-root"),
    path("api/", include("users.urls")),
    path('api/lms/', include('lms.urls')),
]
