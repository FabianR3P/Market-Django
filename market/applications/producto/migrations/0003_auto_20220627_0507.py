# Generated by Django 3.0.6 on 2022-06-27 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0002_auto_20220603_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='count',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='cantidad en almacen'),
        ),
    ]
