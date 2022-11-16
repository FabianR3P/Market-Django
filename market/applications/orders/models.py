from django.db import models
from django.conf import settings
from django.db.models.signals import pre_delete, post_save
#
from model_utils.models import TimeStampedModel

# local apps
from applications.producto.models import Product
from applications.users.models import User
from .managers import CarShopOrderManager, OrderManager, ProductManager, OrderDetailManager,ProduceProductManager


#
#from .signals import update_stok_ventas_producto
class Client(TimeStampedModel):
    """Modelo de lista de clientes para pedidos"""
    name = models.CharField('Nombres', max_length=100)
    f_name = models.CharField('Primer apellido', max_length=100)
    l_name = models.CharField('Segundo Apellido', max_length=100)
    nickname =  models.CharField('Usuario', max_length=100)
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=False)
    def __str__(self):
        return str(self.name) + ' - ' + str(self.nickname)

class ProductByClient(TimeStampedModel):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Cliente',
        related_name='clienteOrder'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='producto',
        related_name='product_client'
    )
    price = models.DecimalField(
        'Precio por cliente',
        max_digits=10,
        decimal_places=2
    )

    objects = ProductManager()


class Ruta(TimeStampedModel):
     driver = models.ForeignKey(
         User,
         on_delete=models.CASCADE,
         verbose_name='Conductor',
         related_name='Conductores'
     )
     ruta_name = models.CharField('Nombre de la ruta', max_length=100)

     comen =  models.CharField(
        'Comentarios',
        max_length=100,
        blank=True,
        default='none',
        )
     def __str__(self):

        return str(self.ruta_name) + ' -- ' + str(self.driver.full_name)

class Order(TimeStampedModel):
    date_order_start = models.DateTimeField(
        'Fecha de Venta',
    )
    cod = models.CharField(
        'codigo de orden',
        max_length=13,
        unique=False,
        blank=True,
        null= True,
    )
    count = models.PositiveIntegerField('Cantidad de Productos')
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Cliente',
        related_name='cliente'
    )
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            verbose_name='cajero',
            blank=True,
            null= True
    )

    amount = models.DecimalField(
        'Monto',
        max_digits=10,
        decimal_places=2
    )

    pay_ammount = models.DecimalField(
        'Monto dejado',
        max_digits=10,
        decimal_places=2
    )
    pend_ammount = models.DecimalField(
        'Monto Pendiente',
        max_digits=10,
        decimal_places=2
    )
    total_pay = models.BooleanField(
        'Pagada',
        default=False
    )
    date_order = models.DateField(
        'Fecha de entrega de pedido',
    )
    time = models.TimeField(
        'Hora del pedido',
        blank=True,
        null= True,
    )
    day_night = models.BooleanField(
        'Pedido tarde o de mañana False = Mañana True = tarde',
        default=False,
    )
    complete = models.BooleanField(
        'Pedido completo',
        default=False
    )
    anulate = models.BooleanField(
        'Venta Anulada',
        default=False,
    )

    objects = OrderManager()

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
    def __str__(self):
            return str(self.id) + ' - ' + str(self.client) + ' - ' + str(self.amount)

class OrderDetail(TimeStampedModel):
    """Modelo que representa a una venta en detalle"""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='producto',
        related_name='product_order'
    )
    ruta = models.ForeignKey(
        Ruta,
        on_delete=models.CASCADE,
        verbose_name='Ruta',
        related_name='Rutas'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Codigo de Venta',
        related_name='detail_sale'
    )
    count = models.PositiveIntegerField('Cantidad')
    select_product = models.CharField(
        'Especificar el tipo de pan',
        max_length=13,
        unique=False
    )
    price_purchase = models.DecimalField(
        'Precio Compra',
        max_digits=10,
        decimal_places=3
    )
    sub_total = models.DecimalField(
        'Subtotal',
        max_digits=10,
        decimal_places=3,
        blank=True,
        null= True,
    )
    price_sale = models.DecimalField(
        'Precio Venta',
        max_digits=10,
        decimal_places=2
    )
    comen =  models.CharField(
        'Comentarios',
        max_length=100,
        blank=True,
        default='none',
    )
    tax = models.DecimalField(
        'Impuesto',
        max_digits=5,
        decimal_places=2
    )
    anulate = models.BooleanField(default=False)
    finish = models.BooleanField(
        'pagado y entegado',
        default=False
    )
    produce = models.BooleanField(
        'Por producir',
        default=False
    )
    contar = models.BooleanField(
        'Por producir',
        default=False
    )


    objects = OrderDetailManager()

    class Meta:
        verbose_name = 'Detalle del pedido'
        verbose_name_plural = 'Detalles de los pedidos'

    def __str__(self):
        return str(self.order.id) + ' - ' + str(self.product.name)


class OrderCarShop(TimeStampedModel):
    """Modelo que representa el carrito de pedidos"""
    barcode = models.CharField(
        max_length=13,
        unique=False
    )
    product = models.ForeignKey(
        ProductByClient,
        on_delete=models.CASCADE,
        verbose_name='producto',
        related_name='product_car'
    )
    count = models.PositiveIntegerField('Cantidad')
    #agregado para tener varios caritos a la vez
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            verbose_name='cajero',
            blank=True,
            null= True
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Cliente',
        related_name='clienteOrderCarshop'
    )
    price = models.DecimalField(
        'Precio',
        max_digits=10,
        decimal_places=3,
        blank=True,
        null= True
    )

    sub_total = models.DecimalField(
        'Subtotal',
        max_digits=10,
        decimal_places=3,
        blank=True,
        null= True,
    )
    comen =  models.CharField(
        'Comentarios',
        max_length=100,
        blank=True,
        null= True,
        default='Sin especificar',
    )

    # numero de usuarios
    User_one = '0'
    User_two = '1'
    User_three = '2'
    #
    TIPO_USERS_CHOICES = [
    (User_one,'USUARIO_1'),
    (User_two,'USUARIO_2'),
    (User_three,'USUARIO_3'),
        ]

    number_shop = models.CharField(
        'USERS',
        blank=True,
        max_length=2,
        default='0',
        choices=TIPO_USERS_CHOICES,
        )

    objects = CarShopOrderManager()

    class Meta:
        verbose_name = 'Carrito de pedidos'
        verbose_name_plural = 'Carrito de pedidos'
        ordering = ['-created']

    def __str__(self):
        return str(self.product.product.name)
    
class ProduceProduct(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='productoProduce',
        related_name='product_produce'
    )
    count = models.PositiveIntegerField('Cantidad')
    produce = models.BooleanField(
        'Por producir',
        default=True
    )
    objects = ProduceProductManager()

