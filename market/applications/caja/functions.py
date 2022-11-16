#
from django.db.models import Prefetch, F, FloatField, ExpressionWrapper
#
from applications.venta.models import Sale, SaleDetail


def detalle_ventas_no_cerradas(id_user):
    # recuepramos arry de id de ventas no cerradas
    ventas = Sale.objects.ventas_no_cerradas(id_user)
    print(ventas)
    consulta = ventas.prefetch_related(
        Prefetch(
            'detail_sale',
            queryset=SaleDetail.objects.filter(sale__id__in=ventas).annotate(
                subtotal=ExpressionWrapper(
                    F('price_sale')*F('count'),
                    output_field=FloatField()
                )
            )
        )
    )

    return consulta

def detalle_ventas_no_cerradas_all():
    # recuepramos arry de id de ventas no cerradas
    ventas = Sale.objects.ventas_no_cerradas_all()
    print(ventas)
    consulta = ventas.prefetch_related(
        Prefetch(
            'detail_sale',
            queryset=SaleDetail.objects.filter(sale__id__in=ventas).annotate(
                subtotal=ExpressionWrapper(
                    F('price_sale')*F('count'),
                    output_field=FloatField()
                )
            )
        )
    )

    return consulta
