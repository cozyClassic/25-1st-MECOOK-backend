from django.urls import path

from .views      import LikeView, AllLikeView

urlpatterns = [
        path('user/like', LikeView.as_view()),
        path('public/like', AllLikeView.as_view())
]