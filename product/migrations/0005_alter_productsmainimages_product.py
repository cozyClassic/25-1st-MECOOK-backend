# Generated by Django 3.2.7 on 2021-10-08 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_productdetailattrs_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsmainimages',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_main_images', to='product.products'),
        ),
    ]
