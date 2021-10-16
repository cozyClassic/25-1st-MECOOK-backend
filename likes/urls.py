from django.urls import path

from .views      import LikeView

urlpatterns = [
    path('/user', LikeView.as_view())
]