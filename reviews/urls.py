from django.urls import path
from .views      import ReviewView, GetReviewView

urlpatterns = [
        path('/comment', ReviewView.as_view()),
        path('/list/<int:product_id>', GetReviewView.as_view()),
        # path('review/<int:review_id>', EditReviewView.as_view())      
]