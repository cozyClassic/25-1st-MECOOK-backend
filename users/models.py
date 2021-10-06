from django.db import models

class User(models.Model):
    account      = models.CharField(max_length=100)
    password     = models.CharField(max_length=100)
    name         = models.CharField(max_length=100)
    gender       = models.CharField(max_length=100)
    nationality  = models.CharField(max_length=100)
    birth_date   = models.DateField()
    phone_number = models.CharField(max_length=50)
    email        = models.CharField(max_length=100)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'