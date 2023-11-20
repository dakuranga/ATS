
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class AllowInactiveUserModelBackend(ModelBackend):
    def user_can_authenticate(self, user):
        return True

def get_user(user_id):
    User = get_user_model()
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return None
