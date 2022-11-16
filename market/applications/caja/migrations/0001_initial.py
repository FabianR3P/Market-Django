# Generated by Django 3.0.6 on 2021-11-13 23:26

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CloseBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('date_close', models.DateTimeField(verbose_name='Fecha de Cierre')),
                ('count', models.PositiveIntegerField(verbose_name='Cantidad de ventas')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Monto total en ventas')),
            ],
            options={
                'verbose_name': 'Cierre Caja',
                'verbose_name_plural': 'Cirres de Caja',
            },
        ),
    ]
