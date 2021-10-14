from django.db import models

class OrderStatus(models.Model) :# 주문완료, 결제완료, 배송중, 주문취소, 배송완료
    order_status    = models.CharField(max_length=50)

    class Meta :
        db_table = 'order_status'

class Orders(models.Model) :
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE)
    order        = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)
    created_at   = models.DateField(auto_now_add=True)
    updated_at   = models.DateField(auto_now=True)

    class Meta :
        db_table = 'orders'

class OrderItems(models.Model) :
    product     = models.ForeignKey('product.Products', on_delete=models.CASCADE)
    order       = models.ForeignKey('Orders', on_delete=models.CASCADE)
    quantity    = models.IntegerField()
    price       = models.DecimalField(default=0, decimal_places=3, max_digits=10)
    created_at  = models.DateField(auto_now_add=True)
    updated_at  = models.DateField(auto_now=True)

    class Meta :
        db_table = 'order_items'