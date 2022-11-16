 # python
from datetime import timedelta
# django
from django.utils import timezone
from django.db import models
#
from applications.producto.models import Product

from django.db.models import Q, Sum, F, FloatField, Case, When
from django.contrib.auth.models import User
import urllib.request

from datetime import timedelta
from django.utils import timezone
import datetime
from datetime import date
from datetime import datetime



class ProductManager(models.Manager):
    """ procedimiento modelo Carrito de pedidos"""
    def productos_cliente(self,id_product,id_client):
        return self.filter(
            product=id_product,
            client_id=id_client,
        )


class OrderManager(models.Manager):
    """ procedimiento modelo Carrito de pedidos"""
    def pedidos_no_cerradas(self):
        return self.filter(
            complete=False,
            anulate=False
        )
    def pedidos_no_cerrada_today(self):
            return self.filter(
                date_order= date.today(),
                complete=False,
                anulate=False
            )
    def pedidos_pendientes(self):
        return self.filter(
            complete=False,
            anulate=False,
        )

    def pedidos_entregados(self):
        return self.filter(
            modified__range= (date.today() + timedelta(hours=1),datetime.now()),
            complete=True,
            anulate=False,
        )

    def monto_pedidos_del_dia(self):

        consulta = self.filter(complete = False).aggregate(
        total=Sum(
            F('amount'),
            output_field=FloatField()
            ),
        )
        print(consulta)
        if consulta['total']:
            return consulta['total']
        else:
            return 0

    def acuenta_pedidos_del_dia(self):
        consulta = self.filter(complete = False).aggregate(
        total=Sum(
            F('pay_ammount'),
            output_field=FloatField()
            ),
        )
        print(consulta)
        if consulta['total']:
            return consulta['total']
        else:
            return 0

    def pendiente_pedidos_del_dia(self):
        consulta = self.filter(complete = False).aggregate(
        total=Sum(
            F('pend_ammount'),
            output_field=FloatField()
            ),
        )
        print(consulta)
        if consulta['total']:
            return consulta['total']
        else:
            return 0
    def restante_pedidos_del_dia(self):
        #Devuelve lo restante de pedidos del día
        consulta = self.filter(complete = True, created__range= (date.today() + timedelta(hours=1),datetime.now())).aggregate(
        total=Sum(
            F('pend_ammount'),
            output_field=FloatField()
            ),
        )
        print('consulta')
        print(consulta)
        if consulta['total']:
            return consulta['total']
        else:
            return 0

class CarShopOrderManager(models.Manager):
    """ procedimiento modelo Carrito de pedidos"""
    #todo el show por elegur que precio usar
    def total_cobrar(self,id):
        print("Entre a la funcion")
        price = 'price'
        consulta = self.filter(client_id = id).aggregate(
            total=Sum(
                F('count')*F('price'),
                output_field=FloatField()
                ),
            )
        print(consulta)
        if consulta['total']:
            return consulta['total']
        else:
            return 0

class OrderDetailManager(models.Manager):
    def total_produccion(self):
        print("Estoy buscando los proudctos encargados  ")
        consulta = self.filter(
                    order__date_order__range = (date.today() + timedelta(hours=1),datetime.now()),
        )
        print(consulta)
        return consulta
    
class ProduceProductManager(models.Manager):
    def total(self):
        print("Estoy buscando los proudctos por producir ")
        consulta = self.filter(
                    created__range = (date.today() + timedelta(hours=1),datetime.now()),
                    produce = True,
        )
        return consulta
