#
from django.urls import path
from . import views

app_name = "venta_app"

urlpatterns = [
    path(
        'venta/index/<id>/<car_num>',
        views.AddCarView.as_view(),
        name='venta-index',
    ),
    path(
        'carshop/update/<pk>/<id_user>/<car_num>',
        views.CarShopUpdateView.as_view(),
        name='carshop-update',
    ),
    path(
        'carshop/updatePlus/<pk>/<id_user>/<car_num>',
        views.CarShopUpdatePlusView.as_view(),
        name='carshop-updatePlus',
    ),
    path(
        'carshop/delete/<pk>/<id_user>/<car_num>',
        views.CarShopDeleteView.as_view(),
        name='carshop-delete',
    ),
    path(
        'carshop/delete-all/<id_user>/<car_num>',
        views.CarShopDeleteAll.as_view(),
        name='carshop-delete_all',
    ),
    path(
        'venta/simple/<id_user>/<car_num>',
        views.ProcesoVentaSimpleView.as_view(),
        name='venta-simple',
    ),
    path(
        'venta/voucher/',
        views.ProcesoVentaVoucherView.as_view(),
        name='venta-voucher',
    ),
    path(
        'venta/voucher-pdf/<pk>/',
        views.VentaVoucherPdf.as_view(),
        name='venta-voucher_pdf',
    ),
    path(
        'venta/ultimas-ventas/<id_user>',
        views.SaleListView.as_view(),
        name='venta-list',
    ),
    path(
        'venta/delete/<pk>/',
        views.SaleDeleteView.as_view(),
        name='venta-delete',
    ),
    path(
        'venta/ticket-venta/<pk>/',
        views.SaleView.as_view(),
        name='venta-ticket',
    ),
]
