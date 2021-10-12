from django.db import models

class Like(models.Model):
    user        = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='like_by_user')
    product     = models.ForeignKey('product.Products', on_delete=models.CASCADE, related_name='like_by_product')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'likes'