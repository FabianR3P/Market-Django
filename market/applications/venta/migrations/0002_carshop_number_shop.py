# Generated by Django 3.0.6 on 2022-04-15 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='carshop',
            name='number_shop',
            field=models.CharField(blank=True, choices=[('0', 'USUARIO_1'), ('1', 'USUARIO_2'), ('2', 'USUARIO_3')], default='0', max_length=2, verbose_name='USERS'),
        ),
    ]
