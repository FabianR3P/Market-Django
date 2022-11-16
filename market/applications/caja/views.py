# django
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    View,
    TemplateView
)
#
from applications.venta.models import Sale, SaleDetail
from applications.users.mixins import VentasPermisoMixin,AdminPermisoMixin
#
from .models import CloseBox
from .functions import detalle_ventas_no_cerradas,detalle_ventas_no_cerradas_all


class ReporteCierreCajaView(AdminPermisoMixin, TemplateView):

    template_name = 'caja/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_user = self.kwargs['id_user']
        context["ventas_dia"] = detalle_ventas_no_cerradas(id_user)
        context["total_vendido"] = Sale.objects.total_ventas_dia(id_user)
        context["total_anulado"] = Sale.objects.total_ventas_anuladas_dia(id_user)
        context["num_ventas_hoy"] = Sale.objects.ventas_no_cerradas(id_user).count()
        return context

class ReporteCierreCajaAllView(AdminPermisoMixin, TemplateView):

    template_name = 'caja/index.html'

    def get_context_data(self):
        context = super().get_context_data()
        context["ventas_dia"] = detalle_ventas_no_cerradas_all()
        context["total_vendido"] = Sale.objects.total_ventas_dia_all()
        context["total_anulado"] = Sale.objects.total_ventas_anuladas_dia_all()
        context["num_ventas_hoy"] = Sale.objects.ventas_no_cerradas_all().count()
        return context

class ReporteCierreCajaView(AdminPermisoMixin, TemplateView):

    template_name = 'caja/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_user = self.kwargs['id_user']
        context["ventas_dia"] = detalle_ventas_no_cerradas(id_user)
        context["total_vendido"] = Sale.objects.total_ventas_dia(id_user)
        context["total_anulado"] = Sale.objects.total_ventas_anuladas_dia(id_user)
        context["num_ventas_hoy"] = Sale.objects.ventas_no_cerradas(id_user).count()
        return context


class ProcesoCerrarCajaView(VentasPermisoMixin, View):

    def post(self, request, *args, **kwargs):
        id_user = self.kwargs['id_user']
        # cerramos las ventas
        num_cerradas, total = Sale.objects.cerrar_ventas()
        if num_cerradas > 0:
            CloseBox.objects.create(
                date_close=timezone.now(),
                count=num_cerradas,
                amount= total,
                user=self.request.user,
            )

        return HttpResponseRedirect(
            reverse(
                'venta_app:venta-index',kwargs={ "id": id_user, "car_num": '0' }
            )
        )
