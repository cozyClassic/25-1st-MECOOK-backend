import jwt

from django.http     import JsonResponse
from mecook.settings import SECRET_KEY, ALGORITHM
from .models         import User

# def login_decorator(func): #데코레이터가 적용된 메소드를 func로 불러옴
#     def wrapper(self, request, *args, **kwargs):

#         if 'Authorization' not in request.headers: #request헤더에 Authorization이 없다면 에러코드 반환
#                                                    #토큰은 HTTP request의 헤더인  Authorization의 value로 옴
#             return JsonResponse({'MESSAGE': 'invalid_user_token'}, status=401)

#         token = request.headers['Authorization'] #token은 value로 오니 딕셔너리 문법에 따름
        
#         try:
#             data = jwt.decode(token, SECRET_KEY, ALGORITHM)
#             user = User.objects.get(id=data['id'])
#             request.user = user
        
#         except jwt.DecodeError:
#             return JsonResponse({'MESSAGE': 'invalid_token'}, status=401)
        
#         except User.DoesNotExist:
#             return JsonResponse({'MESSAGE': 'unknown_user'}, status=401)
        
#         return func(self, request, *args, **kwargs) #조건이 맞으면 시작때 받은 파라미터 돌려줌
#     return wrapper #wrapper함수 리턴. 리턴되는 request는 user객체가 포함된 채로 넘겨짐

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')
            payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            login_user = User.objects.get(id=payload['id'])
            request.user = login_user
        
        except jwt.DecodeError:
            return JsonResponse({'MESSAGE': 'invalid_token'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': 'unknown_user'}, status=401)
        
        return func(self, request, *args, **kwargs)
    return wrapper