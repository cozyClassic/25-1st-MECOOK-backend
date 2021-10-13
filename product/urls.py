from django.urls    import path
from product.views  import DetailByProduct, ListByCategory, ListByLike

urlpatterns = [
    path('/main', ListByLike.as_view()),
    path('/category/<int:category_id>', ListByCategory.as_view()),
    path('/detail/<int:product_id>', DetailByProduct.as_view()),
]