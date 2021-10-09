from django.urls    import path
from product.views  import MenuRaw, CategoryRaw, ProductRaw, CategoryByMenu, ProductByCategory, DetailByProduct, ListByCategory, TestView, ListByLike

urlpatterns = [
    path('/main', ListByLike.as_view()),
    path('/menus', MenuRaw.as_view()),
    path('/menu/categories', CategoryRaw.as_view()),
    path('/menu/category/products', ProductRaw.as_view()),
    path('/menu/<int:category_id>', CategoryByMenu.as_view()),
    path('/menu/<int:category_id>/navbar', ListByCategory.as_view()),
    path('/menu/category/<int:product_id>', ProductByCategory.as_view()),
    path('/menu/category/<int:product_id>/detail', DetailByProduct.as_view()),
    path('/test/<int:category_id>', TestView.as_view()),
]