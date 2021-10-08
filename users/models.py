from django.db import models

class User(models.Model):
    account      = models.CharField(max_length=100)
    password     = models.CharField(max_length=100)
    name         = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50)
    email        = models.CharField(max_length=100)
    points       = models.CharField(max_length=100, default="100,000")
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'