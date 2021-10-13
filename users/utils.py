import jwt

from django.http     import JsonResponse
from mecook.settings import SECRET_KEY, ALGORITHM
from .models         import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')
            payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            login_user = User.objects.get(id=payload['id'])
            request.user = login_user
            user_id = login_user.id
        
        except jwt.DecodeError:
            return JsonResponse({'MESSAGE': 'invalid_token'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': 'unknown_user'}, status=401)
        
        return func(self, request, *args, **kwargs)
    return wrapper