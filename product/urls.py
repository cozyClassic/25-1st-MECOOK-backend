from django.urls    import path
from product.views  import DetailByProduct, ListByCategory, ListByLike, testView

urlpatterns = [
    path('/main', ListByLike.as_view()),
    path('/menu/<int:category_id>/navbar', ListByCategory.as_view()),
    path('/menu/category/<int:product_id>/detail', DetailByProduct.as_view()),
    path('/test/1', testView.as_view())
]