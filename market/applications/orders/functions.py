#
from django.utils import timezone
from django.db.models import Prefetch
#
from applications.producto.models import Product
#
from django.db.models import Q, Sum, F, FloatField, Case, When

from .models import Order, OrderDetail, OrderCarShop,Ruta,ProduceProduct
from .models import Client

import datetime
from datetime import datetime
import requests
import locale
locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))

def contar_produccion(self, **params_entrega):
    print("Entrando al dato final")
    produccion = OrderDetail.objects.total_produccion()
    for producto in produccion:
        if producto.produce == False:
            obj, created = ProduceProduct.objects.get_or_create(
                product=Product.objects.get(barcode=producto.product.barcode),
                defaults={
                    'count' : producto.count,
                }
            )
            if not created:
                print('Estoy modificando la suma porque ya estaba este producto en la cuenta: ')
                print(obj.count)
                print(producto.count)
                obj.count = obj.count + producto.count
                obj.save()
        #produce del detalle del pedido
        producto.produce = True
        producto.save()


def entregar_pedido(self, **params_entrega):
    print("Entrado a la funcion para cerrar el pedido")
    entregado = Order.objects.get(id=params_entrega['pk'] )
    entregado.complete = True
    entregado.pend_ammount = params_entrega['pend_ammount']
    entregado.total_pay = True
    productos_entregados = OrderDetail.objects.filter(order=entregado.id )
    a=True
    ruta_order = 0
    now = datetime.now()
    msg = '👍🏽'  + ' Se ha entregado el pedido de : ' + entregado.client.nickname + ' por: $'+str(entregado.amount)+ ' ' + str(now.strftime("%A, %d de %B de %Y a las %I:%M %p")) + '👍🏽'

    for productos_car in productos_entregados:
        producto = productos_car.product
        print("Se actualiza inventario de :")
        a = producto.count
        print(a)
        if producto.count >= productos_car.count:
            producto.count = producto.count - productos_car.count
            print(producto.count)
            print(producto)
            producto.save()
            a=True
            ruta_order = productos_car.ruta.id
        else:
            a = False
    if a == True:
        if ruta_order != 1:
            msg = '🚚🪗'  + ' Se ha ido el reparto #'+ str(entregado.id) + ' de: '+ entregado.client.nickname + ' por: $'+str(entregado.amount)+ ' ' + str(now.strftime("%A, %d de %B de %Y a las %I:%M %p")) + '🪗🚚'
        else:
            msg = '👍🏽'  + ' Se entrego el pedido #'+ str(entregado.id) + ' de: ' + entregado.client.nickname + ' por: $'+str(entregado.amount)+ ' ' + str(now.strftime("%A, %d de %B de %Y a las %I:%M %p")) + '👍🏽'
        try:
            url = f"https://api.telegram.org/bot5768298048:AAFyjsbxKprBNpSw_VldOM8BxOuEMzNMU0Q/sendMessage"
            response = requests.get(url)
            data = {"chat_id" : "-1001845713292", "text":msg}
            response = requests.post(url,  data=data)
            entregado.save()
        except:
            print("UPS internet de nuevo")
            entregado.save()
    return a

def procesar_pedido(self, **params_pedido):
    # recupera la lista de productos en carrtio
    print("EL PROCESO DE GENERAR UNA ORDEN 2022 AGOSTO")

    productos_en_car = OrderCarShop.objects.filter(client_id=self.kwargs['client_id'])
    client_id = Client.objects.get(id=self.kwargs['client_id']).id


    if productos_en_car.count() > 0:
        hour1= datetime.strptime('12:00:00', '%H:%M:%S').time()
        if params_pedido['hour_order'] < hour1:
            print("El pedido es de la mañana")
            a = False
        else:
            print("El pedido es para la tarde")
            a = True

        # crea el objeto venta
        pedido = Order.objects.create(
            date_order_start=timezone.now(),
            count=0,
            amount=0,
            user=params_pedido['user'],
            pay_ammount=params_pedido['pay_ammount'],
            pend_ammount = params_pedido['pend_ammount'],
            date_order = params_pedido['date_order'],
            time = params_pedido['hour_order'],
            client_id = client_id,
            day_night = a,

        )
        #
        pedidos_detalle = []
        productos_en_pedido = []
        for producto_car in productos_en_car:
            a=producto_car.price
            pedido_detalle = OrderDetail(
                product=producto_car.product.product,
                ruta = Ruta.objects.get(driver__email=params_pedido['ruta']),
                order=pedido,
                count=producto_car.count,
                price_purchase=producto_car.product.product.purchase_price,
                price_sale=a,
                select_product = producto_car.comen,
                tax=0.18,
                sub_total = a*producto_car.count,

                )
            # actualizmos stok de producto en iteracion
            producto = producto_car.product.product
            print('***********PRODUCTO*****************')
            print(producto)
            if( params_pedido['pend_ammount'] == 0 and params_pedido['pay_ammount'] == params_pedido['sub_total'] and params_pedido['finish'] == True):
                producto.count = producto.count - producto_car.count
                producto.num_sale = producto.num_sale + producto_car.count
            #
            pedidos_detalle.append(pedido_detalle)
            productos_en_pedido.append(producto)
            #
            pedido.count = pedido.count + producto_car.count
            #a para seleccionar el costo elegido
            pedido.amount = pedido.amount + producto_car.count*a

        pedido.save()
        OrderDetail.objects.bulk_create(pedidos_detalle)
        # actualizamos el stok
        Product.objects.bulk_update(productos_en_pedido, ['count', 'num_sale'])
        # completada la venta, eliminamos productos delc arrito
        productos_en_car.delete()
        return pedido
    else:
        return None
