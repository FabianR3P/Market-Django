# third-party
from model_utils.models import TimeStampedModel
# Django
from django.db import models
# local
from .managers import ProductManager, CountManager
# Other applications
from applications.users.models import User


class Marca(TimeStampedModel):
    """
        Marca de un producto
    """

    name = models.CharField(
        'Nombre',
        max_length=30
    )

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.name


class Provider(TimeStampedModel):
    """
        Proveedore de Producto
    """

    name = models.CharField(
        'Razon Social',
        max_length=100
    )
    email = models.EmailField(
        blank=True,
        null=True,
    )
    phone = models.CharField(
        'telefonos',
        max_length=40,
        blank=True,
    )
    web = models.URLField(
        'sitio web',
        blank=True,
    )


    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    """Producto"""
    UNIT_CHOICES = (
        ('0', 'Kilogramos'),
        ('1', 'Litros'),
        ('2', 'Unidades'),
    )

    IMPORTANT_CHOICES = (
        ('0', 'Más vendido'),
        ('1', 'Abarrotes'),
        ('2', 'Pan'),
        ('3', 'Lacteos'),
        ('4', 'Pan de Temporada'),
    )

    barcode = models.CharField(
        max_length=13,
        unique=True
    )
    name = models.CharField(
        'Nombre',
        max_length=40
    )
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE
    )
    marca = models.ForeignKey(
        Marca,
        on_delete=models.CASCADE
    )

    due_date = models.DateField(
        'fehca de vencimiento',
        blank=True,
        null=True
    )
    description = models.TextField(
        'descripcion del producto',
        blank=True,
    )
    unit = models.CharField(
        'unidad de medida',
        max_length=1,
        choices=UNIT_CHOICES,
    )

    select_use = models.CharField(
        'Orden de venta',
        max_length=1,
        choices=IMPORTANT_CHOICES,
        blank=True,
        null=True
    )

    count =  models.DecimalField(
        'cantidad en almacen',
        default=0,
        max_digits=7,
        decimal_places=2,
    )
    
    percent =  models.DecimalField(
        'porcentaje de ganancia',
        default=0,
        max_digits=7,
        decimal_places=2,
    )
    purchase_price = models.DecimalField(
        'precio compra',
        max_digits=7,
        decimal_places=2
    )
    sale_price = models.DecimalField(
        'precio venta',
        max_digits=7,
        decimal_places=2
    )
    sale_price1 = models.DecimalField(
        'precio venta1',
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True
    )
    sale_price2 = models.DecimalField(
        'precio venta2',
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True
    )
    sale_price3 = models.DecimalField(
        'precio venta3',
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True
    )
    sale_price4 = models.DecimalField(
        'precio venta4 ',
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True
    )
    sale_last = models.DecimalField(
        'precio pan frio ',
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True
    )
    num_sale = models.PositiveIntegerField(
        'numero de ventas',
        default=0
    )
    anulate = models.BooleanField(
        'eliminado',
        default=False
    )

    #
    objects = ProductManager()

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.name
    
class Subproduct(TimeStampedModel):
    name = models.CharField(
        'Nombre',
        max_length=40
    )
    producto = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return self.name
    
class Count(TimeStampedModel):
    """Control de entradas y salidas."""
    COMMENT_CHOICES = (
        ('0','Pruebas del sistema'),
        ('1', 'Merma'),
        ('2', 'Entrada del día'),
        ('3', 'Baja por mala produccion'),
        ('4', 'Entrada por ajuste de sistema'),
        ('5', 'Baja por consumo de personal'),
        ('6', 'Entrada por cambio de pieza'),
        ('7', 'Baja por cambio de pieza'),
        ('8', 'Entrada de San Miguel'),
        ('9', 'Baja por error'),
        ('10', 'Entrada por ajuste de sistema'),
        ('11', 'Baja por consumo interno'),
        ('12', 'Entrada stock de sistema'),
        ('13', 'Baja por ajuste sistema'),
        
    )
    count_product = models.PositiveIntegerField(
        'Cantidad a modificar',
        default=0
    )
    product = models.ForeignKey(
        Product,
        related_name='Producto',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name='Ingresa',
        on_delete=models.CASCADE
    )

    add_quit = models.BooleanField(
        'Agregar quitar',
        default=True
    )

    comment = models.CharField(
        'Motivo de baja o alta',
        max_length=2,
        choices=COMMENT_CHOICES,
        default=2

    )
    user_produce = models.ForeignKey(
        User,
        related_name='Producción',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    ok = models.BooleanField(
        'contado',
        default=False
    )
    objects = CountManager()

    
class ListFinal(TimeStampedModel):
    """reporte de panes"""
    barcode = models.CharField(
        max_length=13,
        unique=False
    )
    product_report = models.ForeignKey(
        Product,
        related_name='Producto_report',
        on_delete=models.CASCADE
    )
    product_produce = models.DecimalField(
        'cantidad producida al día',
        default=0,
        max_digits=7,
        decimal_places=2
    )
    count_report = models.DecimalField(
        'cantidad en almacen',
        default=0,
        max_digits=7,
        decimal_places=2
    )
    count_add_report = models.DecimalField(
        'cantidad contada',
        default=0,
        max_digits=7,
        decimal_places=2
    )
    count_total_report = models.DecimalField(
        """cantidad sobrante o faltante""",
        default=0,
        max_digits=7,
        decimal_places=2
        )
