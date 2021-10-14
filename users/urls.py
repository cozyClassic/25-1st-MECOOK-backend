from django.urls import path
from users.views import *

urlpatterns = [
        path('/signup', SignupView.as_view()),
        path('/signup/check', CheckView.as_view()),
        path('/login', LoginView.as_view())
]