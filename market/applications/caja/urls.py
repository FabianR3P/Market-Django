#
from django.urls import path
from . import views

app_name = "caja_app"

urlpatterns = [
    path(
        'cierre-caja/index/<id_user>',
        views.ReporteCierreCajaView.as_view(),
        name='caja-index',
    ),
    path(
        'cierre-caja-all',
        views.ReporteCierreCajaAllView.as_view(),
        name='caja-index-all',
    ),
    path(
        'cierre-caja/cerrar/<id_user>',
        views.ProcesoCerrarCajaView.as_view(),
        name='caja-cerrar',
    ),
]
