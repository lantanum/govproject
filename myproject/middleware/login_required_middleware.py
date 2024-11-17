from django.shortcuts import redirect
from django.conf import settings

class LoginRequiredMiddleware:
    PUBLIC_PATHS = ['/accounts/login/','/admin/']  # Пути, доступные без авторизации

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not any(request.path.startswith(path) for path in self.PUBLIC_PATHS):
            return redirect(settings.LOGIN_URL)
        return self.get_response(request)
