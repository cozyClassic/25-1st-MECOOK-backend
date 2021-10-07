from django.db import models

class Like(models.Model):
    user        = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product     = models.ForeignKey('product.Products', on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'likes'