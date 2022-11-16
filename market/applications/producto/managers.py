# python
from datetime import timedelta
# django
from django.db import models
from django.utils import timezone
from django.db.models import Q, F,Sum, FloatField

from datetime import timedelta
from django.utils import timezone
import datetime
from datetime import date
from datetime import datetime

class ProductManager(models.Manager):
    """ procedimiento modelo product """

    def buscar_producto(self, kword, order,select_use):
        consulta = self.filter(
            Q(name__icontains=kword) | Q(barcode=kword)
                    )
        # verificamos en que orden se solicita
        if order == 'date':
            # ordenar por fecha
            return consulta.order_by('created')
        elif order == 'name':
            # ordenar por nombre
            return consulta.order_by('name')
        elif order == 'select_use':
            # ordenar por nombre
            consulta=self.filter(select_use = 0,).order_by('id')
            return  consulta
        elif order == '3':
            # ordenar por lacteos
            print("mandando lacteos")
            consulta=self.filter(select_use = 3,).order_by('id')
            return  consulta

        elif order == '4':
            # ordenar por pan de temporada
            consulta=self.filter(select_use = 4,).order_by('id')
            return  consulta
        elif order == 'stok':
            return consulta.order_by('count')
        else:
            return consulta.order_by('-created')

    def update_stok_ventas_producto(self, venta_id):
        #
        consulta = self.filter(
            product_sale__sale__id=venta_id
        )
        #
        consulta.update(count=(F('count') + 1))

    def productos_en_cero(self):
        #
        consulta = self.filter(
           count__lt=10
        )
        #
        return consulta

    def filtrar(self, **filters):
        if not filters['date_start']:
            filters['date_start'] = '2020-01-01'

        if not filters['date_end']:
            filters['date_end'] = timezone.now().date() + timedelta(1080)
        #
        consulta = self.filter(
            due_date__range=(filters['date_start'], filters['date_end'])
        ).filter(
            Q(name__icontains=filters['kword']) | Q(barcode=filters['kword'])
        ).filter(
            marca__name__icontains=filters['marca'],
            provider__name__icontains=filters['provider'],
        ).filter(
            select_use='0',
        )

        if filters['order'] == 'name':
            return consulta.order_by('name')
        elif filters['order'] == 'stok':
            return consulta.order_by('count')
        elif filters['order'] == 'num':
            return consulta.order_by('-num_sale')
        else:
            return consulta.order_by('-created')
        
class CountManager(models.Manager):
    """ procedimiento modelo product """
    now = datetime.now()
    yesterday = now - timedelta(hours=14)

    def total_ingreso_dia_pan(self,id_producto):
        
        print("************Pruebas de tiempo**********************")
        a= '2022-08-27'
        print(a)
        #print(datetime.date.today())
        consulta = self.filter(
            product_id = id_producto,
            add_quit = True,
            created__range = (date.today(),date.today() + timedelta(hours=24))
            #screated__range = (datetime.date.today() - timedelta(hours=24),datetime.date.today())

        ).aggregate(
            total=Sum('count_product')
        )
        if consulta['total']:
            return consulta['total']
        else:
            return 0

    def total_ingreso_dia(self,barcode):
        #busca el producto por el id
        consulta = self.filter(
                    ok = False,
                    product__barcode = barcode,
                    add_quit = True,
                    created__range = (date.today() + timedelta(hours=1) ,datetime.now())

        ).aggregate(
        total = Sum(
            F('count_product'),
            output_field=FloatField()
            ),
        )
        if consulta['total']:
            return consulta['total']
        else:
            return 0

    def total_baja_dia(self,barcode):
        consulta = self.filter(
                    ok = False,
                    product__barcode = barcode,
                    add_quit = False,
                    created__range = (date.today() + timedelta(hours=1) ,datetime.now())

        ).aggregate(
        total = Sum(
            F('count_product'),
            output_field=FloatField()
            ),
        )
        if consulta['total']:
            return consulta['total']
        else:
            return 0
        #Detalles de entradas y salidas
