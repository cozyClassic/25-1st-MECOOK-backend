import json, re, bcrypt, jwt

from django.http      import JsonResponse
from django.views     import View
from .models          import User
from mecook.settings  import SECRET_KEY, ALGORITHM

class SignupView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            account  = data['account']
            password = data['password']
            email    = data['email']

            if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return JsonResponse({'MESSAGE' : 'invalid_email_format'}, status=400)

            if not re.match('^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}', password):
                return JsonResponse({'MESSAGE' : 'invalid_password_format'}, status=400)

            if User.objects.filter(account = account).exists():
                return JsonResponse({'MESSAGE': 'existing_id'}, status=400)
            
            if User.objects.filter(email = email).exists():
                return JsonResponse({'MESSAGE': 'email_occupied'}, status=400)

            hashed_password   = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_password  = hashed_password.decode('utf-8')

            User.objects.create(
                    account      = account,
                    password     = decoded_password,
                    name         = data['name'],
                    # phone_number = data['phone_number'],
                    email        = email
                )

            return JsonResponse({'MESSAGE': 'signup_success'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': 'key_error'}, status=400)

class LoginView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            account  = data['account']
            password = data['password']

            if not User.objects.filter(account=account).exists():
                return JsonResponse({'MESSAGE': 'invalid_id'}, status=400)
            
            user = User.objects.get(account=account)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'MESSAGE': 'invalid_password'}, status = 400)
            
            access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)

            return JsonResponse({'TOKEN': access_token}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': 'key_error'}, status=400)