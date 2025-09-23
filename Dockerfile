FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Создайте пользователя и директории
RUN adduser --disabled-password --gecos '' appuser && \
    mkdir -p /app && \
    mkdir -p /app/staticfiles

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Установите права на все файлы
RUN chown -R appuser:appuser /app

# Переключитесь на пользователя
USER appuser

EXPOSE 8000



CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]