# Generated by Django 3.0.6 on 2022-10-04 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_produceproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produceproduct',
            name='produce',
            field=models.BooleanField(default=True, verbose_name='Por producir'),
        ),
    ]
