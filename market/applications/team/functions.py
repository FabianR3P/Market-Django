#
from django.utils import timezone
from django.db.models import Prefetch
#
from applications.producto.models import Product
#
from .models import Sale_team, SaleDetail, CarShop_team

from applications.users.models import User
def procesar_venta(self, **params_venta):
    # recupera la lista de productos en carrtio
    print("EL PROCESO CIERRE DE DEUDA DE EMPLEADOS")
    productos_en_car = CarShop_team.objects.filter(number_shop=self.kwargs['car_num'],team_user=self.kwargs['user_team'])
    print(productos_en_car )
    if productos_en_car.count() > 0:
        team_user=self.kwargs['user_team']
        # crea el objeto venta
        venta = Sale_team.objects.create(
            date_sale=timezone.now(),
            count=0,
            amount=0,
            type_invoce=params_venta['type_invoce'],
            type_payment=params_venta['type_payment'],
            user=params_venta['user'],
            team_user_id=User.objects.get(id=team_user).id,
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


            venta_detalle = SaleDetail(
                product=producto_car.product,
                sale=venta,
                count=producto_car.count,
                price_purchase=producto_car.product.purchase_price,
                price_sale=a,
                tax=0.18,
            )
            # actualizmos stok de producto en iteracion
            producto = producto_car.product
            #producto.count = producto.count - producto_car.count
            #suma de las ventas de cada producto
            #producto.num_sale = producto.num_sale + producto_car.count
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
