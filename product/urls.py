from django.urls    import path
from product.views  import CategoryList, ProductList, MenuList

urlpatterns = [
    path('/category', CategoryList.as_view(), name = 'category'),
    path('/menu', MenuList.as_view(), name = 'menu'),
    path('/product_all', ProductList.as_view(), name='products_all'),
]
