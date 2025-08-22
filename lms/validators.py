import re
from rest_framework import serializers


class VideoLinkValidator:
    """
    Проверяет, что ссылка ведёт только на youtube.com
    """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if value:
            youtube_pattern = r'(https?://)?(www\.)?(youtube|youtu\.be)'
            if not re.match(youtube_pattern, value):
                raise serializers.ValidationError(
                    f"В поле {self.field} разрешены только ссылки на YouTube."
                )
