from django.urls    import path
from product.views  import CategoryList, ProductList

urlpatterns = [
    path('product/category/', CategoryList.as_view(), name = 'category'),
]
