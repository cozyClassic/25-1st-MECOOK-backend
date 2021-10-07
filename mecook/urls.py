from django.urls    import path
from product.views  import CategoryList, MenuList, ProductList, MenuByCategory,ListByCategory,DetailByProduct

urlpatterns = [
    path('product/menu_raw/', MenuList.as_view(), name = 'menu'),
    path('product/category_raw/', CategoryList.as_view(), name = 'category'),
    path('product/product_raw/', ProductList.as_view(), name = 'product_all'),
    path('product/product_raw_by_category/<int:category_id>/', MenuByCategory.as_view(), name='menu_good'),
    path('product/category/<int:category_id>/', ListByCategory.as_view(), name='menu_good'),
    path('product/product/<int:product_id>/', DetailByProduct.as_view(), name="product_detail")
]
