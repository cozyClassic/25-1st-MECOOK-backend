from django.urls    import path
from product.views  import DetailByProduct, ListByCategory, ListByLike, ListByKeyword, testView

urlpatterns = [
    path('/main', ListByLike.as_view()),
    path('/menu/<int:category_id>/navbar', ListByCategory.as_view()),
    path('/menu/category/<int:product_id>/detail', DetailByProduct.as_view()),
    path('/search', ListByKeyword.as_view()),
    path('/', testView.as_view()),
]