from django.urls import path

from .views      import LikeView, AllLikeView

urlpatterns = [
        path('/user', LikeView.as_view()),
        path('/public', AllLikeView.as_view())
]