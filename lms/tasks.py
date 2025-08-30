from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Subscription, Course


@shared_task
def send_course_update_notification(course_id):
    try:
        course = Course.objects.get(id=course_id)
        subscribers = Subscription.objects.filter(course=course).select_related("user")

        for subscription in subscribers:
            send_mail(
                subject=f"Курс '{course.title}' обновлён!",
                message=f"Привет, {subscription.user.first_name}!\n\nКурс '{course.title}' был обновлён. Заходи и проверь новые материалы!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscription.user.email],
                fail_silently=False,
            )
    except Course.DoesNotExist:
        pass
