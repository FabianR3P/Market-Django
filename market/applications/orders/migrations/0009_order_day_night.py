# Generated by Django 3.0.6 on 2022-10-15 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_order_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='day_night',
            field=models.BooleanField(default=False, verbose_name='Pedido tarde o de mañana False = Mañana True = tarde'),
        ),
    ]