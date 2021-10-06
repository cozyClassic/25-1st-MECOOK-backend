from django.urls    import path
from product.views  import CategoryList, ProductList, MenuList

urlpatterns = [
    path('product/menu/', MenuList.as_view(), name = 'menu'),
    path('product/category/', CategoryList.as_view(), name = 'category'),
    path('product/product_all/', ProductList.as_view(), name='products_all'),
]
