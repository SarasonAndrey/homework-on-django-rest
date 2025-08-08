from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "preview", "video_url"]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source="lessons", many=True, read_only=True)

    class Meta:
        model = Course
        fields = ["id", "title", "description", "preview", "lesson_count", "lessons"]

    def get_lesson_count(self, obj):
        return obj.lessons.count()
