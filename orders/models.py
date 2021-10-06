from django.db import models

# Create your models here.

class OrderStatusCode(models.Model) :
    order_status    = models.CharField()
    created_at      = models.DateField(auto_now_add=True)
    updated_at      = models.DateField(auto_now=True)

    class Meta :
        db_table = 'order_status_code'


class Orders(models.Model) :
    user_id         = models.ForeignKey('users.User')
    order_status    = models.ForeignKey('OrderStatusCode')
    customer_request= models.TextField(null=True)
    created_at      = models.DateField(auto_now_add=True)
    updated_at      = models.DateField(auto_now=True)

    class Meta :
        db_table = 'orders'

class OrderItemsStatusCode(models.Model) :
    order_items_status  = models.CharField()
    created_at          = models.DateField(auto_now_add=True)
    updated_at          = models.DateField(auto_now=True)

    class Meta :
        db_table = 'order_item_status_code'


class OrderItems(models.Model) :
    product     = models.ForeignKey('product.Product')
    order       = models.ForeignKey('Orders')
    created_at  = models.DateField(auto_now_add=True)
    updated_at  = models.DateField(auto_now=True)

    class Meta :
        db_table = 'order_items'