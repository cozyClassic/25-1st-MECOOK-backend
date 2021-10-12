from django.urls import path

from .views      import LikeView, AllLikeView

urlpatterns = [
        path('/user', LikeView.as_view()),
        path('/public/<int:product_id>', AllLikeView.as_view())
]