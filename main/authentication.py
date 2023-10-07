# main/authentication.py
from django.contrib.auth.backends import ModelBackend
from .models import Fan

from django.contrib.auth.backends import ModelBackend
from .models import Fan


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Fan.objects.get(email=email)
            if user.check_password(password):
                return user
        except Fan.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Fan.objects.get(pk=user_id)
        except Fan.DoesNotExist:
            return None
