#
from django.contrib import admin

from django.urls import path

from . import views


app_name = "orders_app"

urlpatterns = [
    #panel de inicio
    path(
        'orders/index/',
        views.OrdersView.as_view(),
        name='orders-index',
    ),
    #Carrito de compras
    path(
        'orders/car-order/<pk>/',
        views.CarOrdersView.as_view(),
        name='orders-car',
    ),
    #borrar piezas del carrito
    path(
        'orders/delete/<pk>/<id_client>/',
        views.CarShopOrderDeleteView.as_view(),
        name='carshopOrder-delete',
    ),
    #borrar toda la cuenta
    path(
        'orders/delete-all/<id_user>/',
        views.CarShopOrderDeleteAll.as_view(),
        name='carshopOrder-delete_all',
    ),
    #generar el pedido
    path(
        'orders/generate-order/<client_id>/',
        views.ProcesoOrderView.as_view(),
        name='orders-generate',
    ),
    path(
        'orders/list/',
        views.OrderListView.as_view(),
        name='orders-list',
    ),
    path(
        'orders/list-today/',
        views.OrderListTodayView.as_view(),
        name='orders-list-today',
    ),
    path(
        'orders/list-end/',
        views.OrderListEndView.as_view(),
        name='orders-end',
    ),
    path(
        'orders/pedido-view/<order_id>/',
        views.OrderView.as_view(),
        name='orders-view',
    ),
    path(
        'orders/pedido-finish/<order_id>/<client_id>',
        views.FinishOrderView.as_view(),
        name='orders-finish',
    ),
    path(
        'orders/produccion/',
        views.DataView.as_view(),
        name='orders-produccion',
    ),
    path(
        'orders/cerrarDato/',
        views.CerrarDato.as_view(),
        name='orders-cerrar',
    ),


]
