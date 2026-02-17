# user is logged out if their account is inactive for a particular period of time
from django.conf import settings
from django.contrib.auth import logout
from django.utils import timezone
from datetime import timedelta


class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')

            if last_activity:
                last_activity_time = timezone.datetime.fromisoformat(last_activity)
                if timezone.now() - last_activity_time > timedelta(seconds=settings.SESSION_COOKIE_AGE):
                    logout(request)
            request.session['last_activity'] = timezone.now().isoformat()

        return self.get_response(request)
