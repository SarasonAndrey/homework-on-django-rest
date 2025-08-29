from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription

User = get_user_model()


class LessonAndSubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="user@test.com", password="test")
        self.moderator = User.objects.create_user(
            email="moder@test.com", password="test", is_staff=True
        )

        group, _ = Group.objects.get_or_create(name="moderators")
        self.moderator.groups.add(group)

        self.course = Course.objects.create(
            title="Test Course",
            description="Описание",
            owner=self.moderator,
            price=100.00,
        )

        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            video_url="https://youtube.com",
            course=self.course,
            owner=self.moderator,
        )

    def test_lesson_youtube_link_only(self):
        """Только YouTube-ссылки разрешены в video_url."""
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "Bad Link",
            "video_url": "https://example.com",
            "course": self.course.id,
        }
        response = self.client.post("/api/lessons/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lesson_create_valid_link(self):
        """Можно создать урок с YouTube-ссылкой."""
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "Good Lesson",
            "video_url": "https://youtube.com",
            "course": self.course.id,
        }
        response = self.client.post("/api/lessons/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subscribe_unsubscribe_flow(self):
        """Подписка и отписка работают корректно."""
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            f"/api/lms/courses/{self.course.id}/toggle-subscription/"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        response = self.client.post(
            f"/api/lms/courses/{self.course.id}/toggle-subscription/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        def test_course_contains_is_subscribed(self):
            """Сериалайзер возвращает признак is_subscribed."""
            self.client.force_authenticate(user=self.user)
            response = self.client.get("/api/courses/")
            self.assertIn("is_subscribed", response.data["results"][0])

        def test_pagination_applied(self):
            """Пагинация возвращает page_size элементов."""
            self.client.force_authenticate(user=self.user)
            for _ in range(6):
                Lesson.objects.create(
                    title="Extra",
                    video_url="https://youtube.com",
                    course=self.course,
                    owner=self.user,
                )
            response = self.client.get("/api/lessons/?page_size=5")
            self.assertEqual(len(response.data["results"]), 5)
