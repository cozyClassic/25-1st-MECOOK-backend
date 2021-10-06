from django.urls    import path
from product.views  import CategoryList

urlpatterns = [
    path('product/category/', CategoryList.as_view(), name = 'category')
]
