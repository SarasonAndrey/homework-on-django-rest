from django.http import HttpResponse


def api_root(request):
    return HttpResponse(
        """
        <h1>Добро пожаловать в API!</h1>
        <p>Доступные эндпоинты:</p>
        <ul>
            <li><a href='/api/courses/'>Курсы</a></li>
            <li><a href='/api/lessons/'>Уроки</a></li>
        </ul>
        """,
        content_type="text/html; charset=utf-8",
    )
