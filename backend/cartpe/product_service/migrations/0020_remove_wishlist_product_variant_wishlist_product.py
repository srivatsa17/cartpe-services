# Generated by Django 4.2 on 2024-02-23 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_service', '0019_remove_wishlist_product_wishlist_product_variant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='product_variant',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to='product_service.product'),
            preserve_default=False,
        ),
    ]
