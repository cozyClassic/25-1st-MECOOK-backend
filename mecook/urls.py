from django.urls import path, include

urlpatterns = [
    path('user', include('users.urls')),
    path('product', include('product.urls')),
    path('like', include('likes.urls'))
]