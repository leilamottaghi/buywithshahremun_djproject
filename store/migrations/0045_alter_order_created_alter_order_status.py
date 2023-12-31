# Generated by Django 4.1.6 on 2023-03-11 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0044_alter_address_address_alter_address_address_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('awaiting_payment', 'Awaiting Payment'), ('paid', 'Paid'), ('ready_to_send', 'Ready to send'), ('posted', 'Posted'), ('Completed', 'Completed'), ('refunded', 'Refunded'), ('stale', 'Stale')], default='awaiting_payment', max_length=20, verbose_name='وضعیت  سفارش'),
        ),
    ]
