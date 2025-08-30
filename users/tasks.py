from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta


@shared_task
def deactivate_inactive_users():
    User = get_user_model()
    month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=month_ago, is_active=True)

    count = inactive_users.update(is_active=False)

    print(f"Деактивировано {count} неактивных пользователей")
