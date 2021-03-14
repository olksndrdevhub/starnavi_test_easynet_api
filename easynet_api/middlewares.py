import jwt
import traceback

from django.conf import LazySettings, settings
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model



User = get_user_model()
settings = LazySettings()


class LastRequestTimeMiddleware(MiddlewareMixin):

    def process_request(self, request):
        user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))
        if user.is_authenticated:
            user.last_request_time = now()
            user.save()
            request.user = user
        

    @staticmethod
    def get_jwt_user(request):

        user = get_user(request)
        if user.is_authenticated:
            return user
        data = request.META.get('HTTP_AUTHORIZATION', None)

        user = AnonymousUser()
        if data is not None:
            
            token = str.replace(str(data), 'Bearer ', '')
            
            try:
                decoded_token = jwt.decode(token, settings.SECRET_KEY)
                user = User.objects.get(
                    id=decoded_token['user_id']
                )
            except Exception as e: # NoQA
                traceback.print_exc()
            
        return user