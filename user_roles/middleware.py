from django.utils import timezone
from .models import UserLog

class UserLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            if request.path.startswith('/admin/'):  # Example: Capture admin actions
                action = f'Admin action: {request.method} {request.path}'
                UserLog.objects.create(user=request.user, action=action)

        return response
