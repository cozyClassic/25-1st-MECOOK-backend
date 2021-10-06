from django.urls    import path
from product.views  import CategoryList, MenuList, ProductList, MenuByCategory,ListByCategory,DetailByProduct

urlpatterns = [
    path('product/category/', CategoryList.as_view(), name = 'category'),
    path('product/menu/', MenuList.as_view(), name = 'menu'),
    path('product/product_all/', ProductList.as_view(), name = 'product_all'),
    path('product/category/all/', MenuByCategory.as_view(), name='menu_by_category'),
    path('product/category/<int:category_id>/', MenuByCategory.as_view(), name='menu_good'),
    path('product/category_list/<int:category_id>/', ListByCategory.as_view(), name='menu_good'),
    path('product/<int:product_id>/', DetailByProduct.as_view(), name="product_detail")
]
