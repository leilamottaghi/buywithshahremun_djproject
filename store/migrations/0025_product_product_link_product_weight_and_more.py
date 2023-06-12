# Generated by Django 4.1.6 on 2023-02-26 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_rename_comment_order_comment_delete_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_link',
            field=models.CharField(default=None, max_length=400),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, default=None, max_length=400),
        ),
    ]