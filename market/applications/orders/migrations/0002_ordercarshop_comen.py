# Generated by Django 3.0.6 on 2022-09-06 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordercarshop',
            name='comen',
            field=models.CharField(blank=True, default='Sin especificar', max_length=100, null=True, verbose_name='Comentarios'),
        ),
    ]
