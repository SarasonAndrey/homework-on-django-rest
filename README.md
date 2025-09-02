# LMS — Учебная платформа на Django REST Framework

## Описание

Сервис для создания и управления курсами с возможностью подписки, оплаты через Stripe и асинхронной рассылки
уведомлений.

## Функционал

- Регистрация и авторизация (JWT)
- CRUD курсов и уроков
- Подписка на курс (единый эндпоинт)
- Оплата курсов через Stripe (создание продукта, цены и сессии)
- Сохранение ID и ссылки на оплату в модели Payment
- Асинхронная рассылка при обновлении курса (Celery)
- Периодическая блокировка неактивных пользователей (не заходили > 30 дней)
- Документация API: Swagger и ReDoc
- Валидация: только YouTube-ссылки
- Тесты с покрытием (отчёт в `htmlcov/`)

## Технологии

- Python, Django, DRF
- JWT (djangorestframework-simplejwt)
- Celery + Redis (фоновые и периодические задачи)
- Stripe (оплата)
- drf-yasg (документация)
- django-cors-headers

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/SarasonAndrey/homework-on-django-rest/
   
   ```
2. Создайте .env в корне проекта:

### Django

SECRET_KEY=ваш_секретный_ключ

DEBUG=True

### Stripe (ключи из тестового режима)

STRIPE_API_KEY=sk_test_51Q...

### Email (для рассылок)

DEFAULT_FROM_EMAIL=test@lms.ru

### Celery + Redis

REDIS_HOST=localhost

REDIS_PORT=6379

CELERY_BROKER_URL=redis://localhost:6379/0

CELERY_RESULT_BACKEND=redis://localhost:6379/0

CELERY_TIMEZONE=Europe/Moscow

3. Установите зависимости:

   ```
   pip install -r requirements.txt
   
   ```

4. Примените миграции:

   ```
   python manage.py migrate
   ```

5. Запустите сервер:

   ```
   python manage.py runserver
   ```

6. Запустите Celery:

   ```
   celery -A config worker -l INFO -P eventlet
   ```

7. Запустите периодические задачи:

   ```
   celery -A config beat -l INFO
   ```

# Документация API

- Swagger: http://127.0.0.1:8000/swagger/

- ReDoc: http://127.0.0.1:8000/redoc/

# Основные эндпоинты

- POST /api/users/register/ — регистрация
- POST /api/users/token/ — получение токена
- GET /api/courses/ — список курсов
- POST /api/lms/courses/1/toggle-subscription/ — подписка/отписка
- POST /api/users/payment/1/ — создать сессию оплаты курса

# Тесты

### Запуск:

   ```
   coverage run --source='.' manage.py test
   ```

### Отчёт:

   ```
   htmlcov/index.html
   ```

# Лицензия

MIT