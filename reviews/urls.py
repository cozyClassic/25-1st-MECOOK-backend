from django.urls import path
from .views      import ReviewView

urlpatterns = [
        path('/comment', ReviewView.as_view()),
        path('/list/<int:review_id>', ReviewView.as_view()),
        path('/comment/<int:product_id>', ReviewView.as_view()),      
]