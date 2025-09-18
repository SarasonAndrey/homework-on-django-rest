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
   
# Запуск через Docker Compose
## Проект использует Docker для развёртывания всех сервисов.
1. Соберите и запустите контейнеры

   ```
   docker-compose up --build -d
   ```
   
2. Примените миграции (если не применены автоматически)
   
   ```
   docker-compose exec web python manage.py migrate
   ```
   
3. Соберите статику

   ```
   docker-compose exec web python manage.py collectstatic --noinput
   ```
   
4. Создайте суперпользователя (для доступа к админке)

   ```
   docker-compose exec web python manage.py createsuperuser
   ```
   
# Проверка работоспособности сервисов
## После запуска проверьте каждый сервис:
1. Проверьте статус контейнеров
   ```
   docker-compose ps
   ```
   Все сервисы должны быть в статусе Up
2. Проверьте логи веб-сервера
   ```
   docker-compose logs web
   ```
   Должно быть: Starting development server at http://0.0.0.0:8000/
3. Проверьте работу Celery
   ```
   docker-compose logs celery
   ```
   Должно быть: celery@... ready.
                Connected to redis://redis:6379/0
4. Проверьте Celery Beat
   ```
   docker-compose logs celery-beat
   ```
   Должно быть: beat: Starting...
                      Scheduler: Ready to go!
5. Проверьте PostgreSQL
   ```
   docker-compose exec db psql -U suser -d online_learning_platform
   ```
   После входа выполните: 
   ```
   \dt
   ```
6. Проверьте Redis
   ```
   docker-compose exec redis redis-cli PING
   ```
   Ожидаемый ответ: PONG

# Доступ к приложению

   Основное приложение: http://localhost:8000

   Админка: http://localhost:8000/admin/

   Swagger: http://localhost:8000/swagger/

   ReDoc: http://localhost:8000/redoc/

# Настройка удалённого сервера (Yandex Cloud)

1. Создана ВМ с Ubuntu 24.04 LTS, 2 vCPU, 2 ГБ RAM
2. Настроен SSH-доступ с использованием RSA-ключа (4096 бит)
3. Установлены:
   - Docker
   - Docker Compose
   - Git
4. Проект развёрнут через ``` docker-compose up --build -d ```
5. Сервер доступен по публичному IP

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