from django.urls    import path
from product.views  import testView

urlpatterns = [
    path('/', testView.as_view()),
]