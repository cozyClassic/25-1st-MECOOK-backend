from django.urls import path
from .views      import ReviewView

urlpatterns = [
        path('/comment', ReviewView.as_view()),
        path('/list', ReviewView.as_view()),      
        path('/comment/<int:review_id>', ReviewView.as_view()),
]