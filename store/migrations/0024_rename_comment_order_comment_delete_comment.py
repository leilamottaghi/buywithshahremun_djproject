# Generated by Django 4.1.6 on 2023-02-25 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_order_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Comment',
            new_name='comment',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]