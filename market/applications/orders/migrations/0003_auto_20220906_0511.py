# Generated by Django 3.0.6 on 2022-09-06 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_ordercarshop_comen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cod',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='codigo de orden'),
        ),
    ]