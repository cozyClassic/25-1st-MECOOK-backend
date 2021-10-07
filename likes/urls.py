from django.urls import path

from .views      import LikeView

urlpatterns = [
        path('like', LikeView.as_view()),
]