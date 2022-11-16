#
from django.utils import timezone
from django.db.models import Prefetch
#
from applications.producto.models import Product
#
from .models import Sale, SaleDetail, CarShop


def procesar_venta(self, **params_venta):
    # recupera la lista de productos en carrtio
    print("EL PROCESO DE VENTA")

    productos_en_car = CarShop.objects.filter(user=self.kwargs['id_user'],number_shop=self.kwargs['car_num'])

    if productos_en_car.count() > 0:

        # crea el objeto venta
        venta = Sale.objects.create(
            date_sale=timezone.now(),
            count=0,
            amount=0,
            type_invoce=params_venta['type_invoce'],
            type_payment=params_venta['type_payment'],
            user=params_venta['user'],
        )
        #
        ventas_detalle = []
        productos_en_venta = []
        for producto_car in productos_en_car:
            if( producto_car.price == 1):
                a=producto_car.product.sale_price
            elif( producto_car.price == 5):
                a=producto_car.product.sale_price1
            elif( producto_car.price == 2):
                a=producto_car.product.sale_price2
            elif( producto_car.price == 3):
                a=producto_car.product.sale_price3
            elif( producto_car.price == 4):
                a=producto_car.product.sale_price4
            elif( producto_car.price == 6):
                a=producto_car.product.sale_last

            venta_detalle = SaleDetail(
                product=producto_car.product,
                sale=venta,
                count=producto_car.count,
                price_purchase=producto_car.product.purchase_price,
                price_sale=a,
                tax=0.18,
                sub_total = a*producto_car.count,

            )
            # actualizmos stok de producto en iteracion
            producto = producto_car.product
            producto.count = producto.count - producto_car.count
            producto.num_sale = producto.num_sale + producto_car.count
            #
            ventas_detalle.append(venta_detalle)
            productos_en_venta.append(producto)
            #
            venta.count = venta.count + producto_car.count
            #a para seleccionar el costo elegido
            venta.amount = venta.amount + producto_car.count*a

        venta.save()
        SaleDetail.objects.bulk_create(ventas_detalle)
        # actualizamos el stok
        Product.objects.bulk_update(productos_en_venta, ['count', 'num_sale'])
        # completada la venta, eliminamos productos delc arrito
        productos_en_car.delete()
        return venta
    else:
        return None
