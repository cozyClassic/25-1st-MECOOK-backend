from django.urls import path
from .views      import ReviewView, GetReviewView, EditReviewView

urlpatterns = [
        path('/comment', ReviewView.as_view()),
        path('/comment/<int:review_id>', EditReviewView.as_view()),
        path('/list/<int:product_id>', GetReviewView.as_view()),      
]