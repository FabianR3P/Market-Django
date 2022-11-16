# Django
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    View,
    FormView,
    TemplateView
)
# local
from applications.venta.models import SaleDetail, Sale
from applications.orders.models import Order

from applications.users.mixins import AlmacenPermisoMixin, AdminPermisoMixin, VentasPermisoMixin
#
from applications.caja.functions import detalle_ventas_no_cerradas,detalle_ventas_no_cerradas_all

from .models import Product, Count, ListFinal
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse


from .forms import ProductForm, CountForm, ReportForm,ReportProductForm
from applications.utils import render_to_pdf

from applications.users.models import User

from django.contrib import messages

import json
import requests
import locale
from datetime import datetime
PROPETIES = 'C:\Django\market\applications\scripts\telegramkeys.txt'
locale.setlocale(locale.LC_ALL, "es_MX")

class AddProductView(AlmacenPermisoMixin, FormView):
    """Modelo de ingreso de pan del día"""
    template_name = 'producto/addB.html'
    form_class = CountForm
    success_url = reverse_lazy('producto_app:producto-lista')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['id_product']
        context["producto"] = Product.objects.filter(id=product_id)
        for product in context["producto"]:
            print(product.name)
            context["venta_count"]= product.count - 1000

        print(context["producto"])
        return context

    def form_valid(self, form,*args, **kwargs):
        a = False
        count_product = form.cleaned_data['count_product']
        #add_quit = form.cleaned_data['add_quit']
        user_id = self.kwargs['id_user']
        product_id = self.kwargs['id_product']
        comment = form.cleaned_data['comment']
        print(comment)
        if int(comment) % 2 == 0:
            print("El nummero es par")
            add_quit = True
        else:
            print("El numero es impar")
            add_quit = False

        user_produce = form.cleaned_data['user_produce']
        product = Product.objects.get(id=product_id)
        p = Count.objects.create(
                    user = User.objects.get(id=user_id),
                    product = Product.objects.get(id=product_id),
                    count_product = count_product,
                    add_quit = add_quit,
                    comment = comment,
                    user_produce = user_produce,
                )
        print('Exixtencia actual')
        print(product.count)
        now = datetime.now()
        if add_quit == True:
            product.count = product.count+count_product
            msg = '✅' + p.get_comment_display() + ' se han agregado: ' + str(count_product) + ' ' + product.name + ' el : ' + str(now.strftime("%A, %d de %B de %Y a las %I:%M %p"))

        else:
            if product.count >= count_product:
                print("se puede quitar")
                product.count = product.count-count_product
                msg = '❌' +  p.get_comment_display() + ' se han dado de baja: ' + str(count_product) + ' ' + product.name + ' el : ' + str(now.strftime("%A, %d de %B de %Y a las %I:%M %p"))
                a=False
            else:
                print("No tienes inventario")
                a=True
        if a == False:
            try:
                url = f"https://api.telegram.org/bot5768298048:AAFyjsbxKprBNpSw_VldOM8BxOuEMzNMU0Q/sendMessage"
                response = requests.get(url)
                data = {"chat_id" : "-1001845713292", "text":msg}
                response = requests.post(url,  data=data)
                print('Existencia modificado')
                print(product.count)
                Product.objects.filter(id=product_id).update(count=product.count)
                return super(AddProductView, self).form_valid(form)
            except:
                print("Algo pasa con el internet")
                Product.objects.filter(id=product_id).update(count=product.count)
                return super(AddProductView, self).form_valid(form)
        else:
            print("No tienes stock"+ product.name)
            messages.warning(self.request, product.name)
            return HttpResponseRedirect(
                reverse(
                    'producto_app:producto-add',kwargs={ "id_product":product_id,"id_user":user_id}
                )
            )


class ProductListView(AlmacenPermisoMixin, ListView):
    template_name = "producto/lista.html"
    context_object_name = 'productos'

    def get_queryset(self):
        kword = self.request.GET.get("kword", '')
        order = self.request.GET.get("order", '')
        select_use=self.request.GET.get("select_use", ''),
        print(select_use)
        queryset = Product.objects.buscar_producto(kword, order,select_use)
        return queryset


class ProductCreateView(AlmacenPermisoMixin, CreateView):
    template_name = "producto/form_producto.html"
    form_class = ProductForm
    success_url = reverse_lazy('producto_app:producto-lista')


class ProductUpdateView(AlmacenPermisoMixin, UpdateView):
    template_name = "producto/form_producto.html"
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('producto_app:producto-lista')



class ProductDeleteView(AlmacenPermisoMixin, DeleteView):
    template_name = "producto/delete.html"
    model = Product
    success_url = reverse_lazy('producto_app:producto-lista')


class ProductDetailView(AlmacenPermisoMixin, DetailView):
    template_name = "producto/detail.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #
        context["ventas_mes"] = SaleDetail.objects.ventas_mes_producto(
            self.kwargs['pk']
        )
        return context
class ReportProduct(AlmacenPermisoMixin,FormView):
    template_name = "producto/report.html"
    form_class = ReportForm
    success_url = reverse_lazy('producto_app:producto-report')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["producto"] = Product.objects.filter(report=True)
        return context

    def form_valid(self, form,*args, **kwargs):

        return super(ReportProduct, self).form_valid(form)


class ProductDetailViewPdf(AlmacenPermisoMixin, View):

    def get(self, request, *args, **kwargs):
        producto = Product.objects.get(id=self.kwargs['pk'])
        data = {
            'product': producto,
            'ventas_mes': SaleDetail.objects.ventas_mes_producto(self.kwargs['pk'])
        }
        pdf = render_to_pdf('producto/detail-print.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


class FiltrosProductListView(AlmacenPermisoMixin, ListView):
    template_name = "producto/filtros.html"
    context_object_name = 'productos'
    def get_queryset(self):
        queryset = Product.objects.filtrar(
            kword=self.request.GET.get("kword", ''),
            date_start=self.request.GET.get("date_start", ''),
            date_end=self.request.GET.get("date_end", ''),
            provider=self.request.GET.get("provider", ''),
            marca=self.request.GET.get("marca", ''),
            order=self.request.GET.get("order", ''),
        )
        return queryset

class ReportListView(VentasPermisoMixin, FormView):

    template_name = 'producto/report_product.html'
    form_class = ReportProductForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["productos"] = ListFinal.objects.all()
        context["ventas_dia"] = detalle_ventas_no_cerradas_all()
        context["total_vendido"] = Sale.objects.total_ventas_dia_all()
        context["total_anulado"] = Sale.objects.total_ventas_anuladas_dia_all()
        context["num_ventas_hoy"] = Sale.objects.ventas_no_cerradas_all().count()
        context["total_pedidos"] = Order.objects.monto_pedidos_del_dia()
        context["acuenta"] = Order.objects.acuenta_pedidos_del_dia()
        context["pendiente"] = Order.objects.pendiente_pedidos_del_dia()
        context["pedidos"] = Order.objects.pedidos_pendientes().count()
        context["restante"] = Order.objects.restante_pedidos_del_dia()
        print(context["productos"])
        return context

    def form_valid(self, form,*args, **kwargs):
        barcode = form.cleaned_data['barcode']
        count_add_report = form.cleaned_data['count']
        producto=Product.objects.get(barcode=barcode)
        product_produce = Count.objects.total_ingreso_dia_pan(producto.id)
        count_almacen = producto.count
        count_t= producto.count - count_add_report
        producto_dia = Count.objects.total_ingreso_dia_pan(producto.id)
        obj, created = ListFinal.objects.get_or_create(
            barcode=barcode,
            #obtencion de datos del productos
            defaults={
                'product_report': Product.objects.get(barcode=barcode),
                'count_add_report': count_add_report,
                'count_report': count_almacen,
                'count_total_report': count_t,
                'product_produce' : product_produce,

            }
        )
        #
        super(ReportListView, self).form_valid(form)
        return HttpResponseRedirect(
            reverse(
                'producto_app:reporte-general',kwargs={ }
            )
        )

class ReportListDeleteView(VentasPermisoMixin, View):
    model = ListFinal
    def post(self, request, *args, **kwargs):
        ListFinal.objects.filter(id=self.kwargs['pk']).delete()
        return HttpResponseRedirect(
            reverse(
                'producto_app:reporte-general',kwargs={ }
            )
        )
class ReportProduccionView(AlmacenPermisoMixin, FormView):

    template_name = 'producto/report_produccion.html'
    form_class = ReportProductForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
            #migajon
        context['migajon'] = Count.objects.total_ingreso_dia('07')
        print(context['migajon'])
        context['por_migajon'] = (context['migajon']*100)/2000
        context['migajon_b'] = Count.objects.total_baja_dia('07')
        context['por_migajon_b'] = (context['migajon_b']*100)/700
        #reposteria
        context['reposteria'] = Count.objects.total_ingreso_dia('10')
        context['por_reposteria'] = (context['reposteria']*100)/2000
        context['reposteria_b'] = Count.objects.total_baja_dia('10')
        context['por_reposteria_b'] = (context['reposteria_b']*100)/700
        #mostrador
        context['mostrador'] = Count.objects.total_ingreso_dia('13')
        context['por_mostrador'] = (context['mostrador']*100)/2000
        context['mostrador_b'] = Count.objects.total_baja_dia('13')
        context['por_mostrador_b'] = (context['mostrador_b']*100)/700
        #variedad
        context['variedad'] = Count.objects.total_ingreso_dia('16')
        context['por_variedad'] = (context['variedad']*100)/2000
        context['variedad_b'] = Count.objects.total_baja_dia('16')
        context['por_variedad_b'] = (context['variedad_b']*100)/700
        #peineta
        context['peineta'] = Count.objects.total_ingreso_dia('37')
        context['por_peineta'] = (context['peineta']*100)/2000
        context['peineta_b'] = Count.objects.total_baja_dia('37')
        context['por_peineta_b'] = (context['peineta_b']*100)/700
        #bolillo
        context['Bolillo'] = Count.objects.total_ingreso_dia('02')
        context['porcentaje'] = (context['Bolillo']*100)/20000
        context['Bolillo_b'] = Count.objects.total_baja_dia('02')
        context['porcentaje_b'] = (context['Bolillo_b']*100)/1500
        #Telera
        context['Telera'] = Count.objects.total_ingreso_dia('01')
        context['por_Telera'] = (context['Telera']*100)/2000
        context['Telera_b'] = Count.objects.total_baja_dia('01')
        context['por_Telera_b'] = (context['Telera_b']*100)/700
        #bolillo_artesanal
        context['bolillo_artesanal'] = Count.objects.total_ingreso_dia('27')
        context['por_bolillo_artesanal'] = (context['bolillo_artesanal']*100)/2000
        context['bolillo_artesanal_b'] = Count.objects.total_baja_dia('27')
        context['por_bolillo_artesanal_b'] = (context['bolillo_artesanal_b']*100)/700
        #bolillo_integral
        context['bolillo_integral'] = Count.objects.total_ingreso_dia('05')
        context['por_bolillo_integral'] = (context['bolillo_integral']*100)/2000
        context['bolillo_integral_b'] = Count.objects.total_baja_dia('05')
        context['por_bolillo_integral_b'] = (context['bolillo_integral_b']*100)/700
        #bolillo_ajonjoli
        context['bolillo_ajonjoli'] = Count.objects.total_ingreso_dia('39')
        context['por_bolillo_ajonjoli'] = (context['bolillo_ajonjoli']*100)/2000
        context['bolillo_ajonjoli_b'] = Count.objects.total_baja_dia('39')
        context['por_bolillo_ajonjoli_b'] = (context['bolillo_ajonjoli_b']*100)/700
        #telera_ajonjoli
        context['telera_ajonjoli'] = Count.objects.total_ingreso_dia('25')
        context['por_telera_ajonjoli'] = (context['telera_ajonjoli']*100)/2000
        context['telera_ajonjoli_b'] = Count.objects.total_baja_dia('25')
        context['por_telera_ajonjoli_b'] = (context['telera_ajonjoli_b']*100)/700
        #español
        context['español'] = Count.objects.total_ingreso_dia('26')
        context['por_español'] = (context['español']*100)/2000
        context['español_b'] = Count.objects.total_baja_dia('26')
        context['por_español_b'] = (context['español_b']*100)/700
        #baguette
        context['baguette'] = Count.objects.total_ingreso_dia('03')
        context['por_baguette'] = (context['baguette']*100)/2000
        context['baguette_b'] = Count.objects.total_baja_dia('03')
        context['por_baguette_b'] = (context['baguette_b']*100)/700
        #pan_muerto
        context['pan_muerto'] = Count.objects.total_ingreso_dia('40')
        context['por_pan_muerto'] = (context['pan_muerto']*100)/2000
        context['pan_muerto_b'] = Count.objects.total_baja_dia('40')
        context['por_pan_muerto_b'] = (context['pan_muerto_b']*100)/700
        #mini_bolillo
        context['mini_bolillo'] = Count.objects.total_ingreso_dia('29')
        context['por_mini_bolillo'] = (context['mini_bolillo']*100)/2000
        context['mini_bolillo_b'] = Count.objects.total_baja_dia('29')
        context['por_mini_bolillo_b'] = (context['mini_bolillo_b']*100)/700
        return context

    def form_valid(self, form,*args, **kwargs):

        super(ReportListView, self).form_valid(form)
        return HttpResponseRedirect(
            reverse(
                'producto_app:reporte-general',kwargs={ }
            )
        )

class ReportProduccionDetailView(AlmacenPermisoMixin, FormView):

    template_name = 'producto/report_produccion_detail.html'
    form_class = ReportProductForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        return context

    def form_valid(self, form,*args, **kwargs):

        super(ReportListView, self).form_valid(form)
        return HttpResponseRedirect(
            reverse(
                'producto_app:reporte-general',kwargs={ }
            )
        )
