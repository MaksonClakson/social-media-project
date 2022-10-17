import jwt
import traceback

from django.utils.functional import SimpleLazyObject
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.conf import LazySettings
from django.contrib.auth.middleware import get_user

settings = LazySettings()


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))

    @staticmethod
    def get_jwt_user(request):
        User = get_user_model()
        user_jwt = get_user(request)
        if user_jwt.is_authenticated:
            return user_jwt
        data = request.META.get('HTTP_AUTHORIZATION', None)

        user_jwt = AnonymousUser()
        if data is not None:
            try:
                token = str.replace(data, 'JWT ', '')
                user_jwt = jwt.decode(
                    token,
                    key=settings.SECRET_KEY,
                    algorithms=['HS256'],
                )
                user_jwt = User.objects.get(
                    id=user_jwt['user_id']
                )
            except Exception as e: # NoQA
                traceback.print_exc()
        return user_jwt