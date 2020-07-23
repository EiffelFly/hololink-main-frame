from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.models import User

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    '''
        Make django built-in user model can be verified with email and username
        at same time.
        https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#writing-an-authentication-backend
    '''

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # we are using username or email to login
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            # when some hacker try to break this violently, we have to make sure every 
            # request to database to be the same
            UserModel().set_password(password)
        except MultipleObjectsReturned:
            return User.objects.filter(email=username).order_by('id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None