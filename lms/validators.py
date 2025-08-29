import re
from rest_framework import serializers


class VideoLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):

        if value and isinstance(value, str):
            youtube_pattern = r"(https?://)?(www\.)?(youtube|youtu\.be)"
            if not re.match(youtube_pattern, value):
                raise serializers.ValidationError(
                    f"Поле {self.field} может содержать только ссылки на YouTube."
                )
        elif value:
            raise serializers.ValidationError(f"Поле {self.field} должно быть строкой.")
