# Generated by Django 4.1.6 on 2023-02-13 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_product_discount_price_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]