from django.db import models

class Orders(models.Model) :
    user            = models.ForeignKey('users.User', on_delete=models.CASCADE)
    cart            = models.ForeignKey('cart.Carts', on_delete=models.CASCADE)
    created_at      = models.DateField(auto_now_add=True)
    updated_at      = models.DateField(auto_now=True)

    class Meta :
        db_table = 'orders'