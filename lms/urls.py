from django.urls import path, include
from .views import toggle_subscription

urlpatterns = [
    path(
        "courses/<int:course_id>/toggle-subscription/",
        toggle_subscription,
        name="toggle-subscription",
    ),
]
