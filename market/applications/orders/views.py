# django
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    View,
    UpdateView,
    DeleteView,
    ListView
)
from django.views.generic.edit import (
    FormView
)
# local
from applications.producto.models import Product, Subproduct
from applications.utils import render_to_pdf
from applications.users.mixins import VentasPermisoMixin
#
#
from django.contrib.auth.models import User

from applications.venta.forms import VentaForm, VentaVoucherForm
from .forms import OrderForm,DetailOrderForm, FinishOrderForm

from .models import Client,ProductByClient,OrderCarShop, Ruta, Order, OrderDetail,ProduceProduct
from .functions import procesar_pedido, entregar_pedido , contar_produccion

from decimal import Decimal
import time
from datetime import date
from datetime import datetime

class OrdersView(VentasPermisoMixin, FormView):
    template_name = 'orders/index.html'
    form_class = VentaForm
    success_url = '.'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clientes"] = Client.objects.all().order_by('nickname')
        #print("Entra a la data")
        return context
    def form_valid(self, form,*args, **kwargs):
        #obtener id de usuario
        return render(request, 'index.html', {'form': form})

#Vista para subir pedidos
class CarOrdersView(VentasPermisoMixin, FormView):
    template_name = 'orders/orders.html'
    form_class = OrderForm
    success_url = '.'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_client = self.kwargs['pk']
        context["datos_cliente"] = Client.objects.filter( id = id_client)
        context["productos_cliente"] = ProductByClient.objects.filter( client = id_client)
        #modificar por cliente
        context["productos_car"] = OrderCarShop.objects.filter( client = id_client)
        #Subproductos
        context["subproductos"] = Subproduct.objects.all()
        #Total de la cuenta
        context["total_cobrar"] = OrderCarShop.objects.total_cobrar(id_client)
        #llama al formulario
        context['form_order'] = DetailOrderForm
        return context

    def form_valid(self, form,*args, **kwargs):
        id_client = self.kwargs['pk']
        barcode = form.cleaned_data['barcode']
        count = form.cleaned_data['count']
        comen = form.cleaned_data['comen']
        print("los datos pra consuta son client_id: " + id_client)
        producto =  ProductByClient.objects.get(product__barcode=barcode, client__id=id_client)
        print("probando consultas de productos: ")
        print(producto)
        sub_total = producto.price * count
        OrderCarShop.objects.create(
            barcode=barcode,
            user=self.request.user,
            product = ProductByClient.objects.get(product__barcode=barcode, client__id=id_client),
            count = count,
            price = producto.price,
            client = Client.objects.get(id = id_client),
            sub_total = sub_total,
            comen = comen,
        )

        super(CarOrdersView, self).form_valid(form)
        return HttpResponseRedirect(
            reverse(
                'orders_app:orders-car',kwargs={ "pk":id_client,}
            )
        )

class CarShopOrderDeleteView(VentasPermisoMixin, View):
    """Quita un producto del carrito"""
    model = OrderCarShop
    def post(self, request, *args, **kwargs):
        OrderCarShop.objects.filter(id=self.kwargs['pk']).delete()
        cliente = self.kwargs['id_client']
        return HttpResponseRedirect(
            reverse(
                'orders_app:orders-car',kwargs={ "pk": cliente,}
            )
        )

class CarShopOrderDeleteAll(VentasPermisoMixin, View):

    def post(self, request, *args, **kwargs):
        print("Tratando de eliminar")
        id_user = self.kwargs['id_user']
        OrderCarShop.objects.filter(user_id = self.request.user).delete()
        #
        return HttpResponseRedirect(
            reverse(
                'orders_app:orders-car',kwargs={ "pk": id_user,}
            )
        )

class ProcesoOrderView(VentasPermisoMixin, FormView):
    form_class = DetailOrderForm
    template_name = 'orders/modal-order.html'
    success_url = '.'

    def get_context_data(self, **kwargs):
        print("Entradno al get context data")
        context = super().get_context_data(**kwargs)
        id_client = self.kwargs['client_id']
        context["datos_cliente"] = Client.objects.filter( id = id_client)
        #modificar por cliente
        context["productos_car"] = OrderCarShop.objects.filter( client = id_client)
        #Total de la cuenta
        context["total_cobrar"] = OrderCarShop.objects.total_cobrar(id_client)
        #llama al las Rutas
        context["Rutas"] = Ruta.objects.all()
        return context

    def form_valid(self, form,*args, **kwargs):
        id_client = self.kwargs['client_id']
        total = OrderCarShop.objects.total_cobrar(id_client)
        pay_ammount = form.cleaned_data['pay_ammount']
        date_order = form.cleaned_data['date_order']
        hour_order = form.cleaned_data['hour_order']
        ruta = form.cleaned_data['ruta']
        finish = form.cleaned_data['finish']
        print("La condicion es: ")
        print(pay_ammount)
        print("menor a; ")
        print(total)
        total_r = round(total)
        pay_ammount_r = round(pay_ammount)
        print(total_r)
        print(pay_ammount_r)
        print(total <= pay_ammount)
        print(pay_ammount <= total)

        if pay_ammount <= total:
            
            pend_ammount = Decimal(total) - pay_ammount
            procesar_pedido(
                self=self,
                pay_ammount = pay_ammount,
                pend_ammount = pend_ammount,
                sub_total = total,
                user=self.request.user,
                date_order = date_order,
                hour_order=hour_order,
                ruta=ruta,
                finish=finish,
            )
            super(ProcesoOrderView, self).form_valid(form)
            return HttpResponseRedirect(
                reverse(
                    'orders_app:orders-index',
                    kwargs={},
                )
            )
        else:
            print("No pude ingresar al if ")
            return HttpResponseRedirect(
                reverse(
                    'orders_app:orders-generate',
                    kwargs={"client_id" : id_client},
                )
            )

class OrderListView(VentasPermisoMixin, ListView):
    template_name = 'orders/pedidos.html'
    context_object_name = "pedidos"
    paginate_by = 40

    def get_queryset(self):
        return Order.objects.pedidos_no_cerradas().order_by("-id")
    
class OrderListTodayView(VentasPermisoMixin, ListView):
    template_name = 'orders/pedidos_today.html'
    context_object_name = "pedidosToday"

    def get_queryset(self):
        return Order.objects.pedidos_no_cerrada_today().order_by("-date_order")

class OrderListEndView(VentasPermisoMixin, ListView):
    template_name = 'orders/pedidos-end.html'
    context_object_name = "pedidos"
    paginate_by = 40

    def get_queryset(self):
        return Order.objects.pedidos_entregados().order_by("-modified")

class OrderView(VentasPermisoMixin, ListView):
    template_name = 'orders/orders-view.html'
    context_object_name = "ventas"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['order_id']
        context['pedido_detail'] = Order.objects.filter(id=pk).order_by("-id")
        context['productos'] = OrderDetail.objects.filter(order_id=pk).order_by("-id")
        print( context['productos'] )
        return context

    def get_queryset(self):
        pk = self.kwargs['order_id']
        return OrderDetail.objects.filter(order_id=pk).order_by("-id")

#PEDIDO ENTREGADO

class FinishOrderView(VentasPermisoMixin, FormView):
    template_name = 'orders/finish-orders.html'
    form_class = FinishOrderForm
    success_url = '.'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['order_id']
        context['pedido_detail'] = Order.objects.filter(id=pk).order_by("-id")
        context['productos'] = OrderDetail.objects.filter(order_id=pk).order_by("-id")
        return context

    def form_valid(self, form,*args, **kwargs):
        pk = self.kwargs['order_id']
        client = self.kwargs['client_id']
        print("*******************Recibiendo datos ***************************")
        pay = form.cleaned_data['pay']
        pedido = Order.objects.get(id=pk)
        print(pedido)
        productos = OrderDetail.objects.filter(order=pedido.id )
        for check in productos:
            print("revisando stock de los productos")
            producto = check.product
            print(producto)
            if producto.count >= check.count:
                print("Tienen inventario")
            else:
                print("no tienes inventario")
                super(FinishOrderView, self).form_valid(form)
                return HttpResponseRedirect(
                    reverse(
                        'orders_app:orders-finish',kwargs={"order_id" : pk, "client_id" : client}
                    )
                )
                break

        if pedido.pend_ammount == pay or pedido.pend_ammount == 0:
            entregar_pedido(
                self=self,
                pk=pk,
                pay = pay,
                client = client,
                pend_ammount=pay,
                )

            print(pay)
            super(FinishOrderView, self).form_valid(form)
            return HttpResponseRedirect(
                reverse(
                    'orders_app:orders-list-today',kwargs={}
                )
            )
        else:
            return HttpResponseRedirect(
                reverse(
                    'orders_app:orders-finish',kwargs={"order_id" : pk, "client_id" : client}
                )
            )


#PEDIDO ENTREGADO
class DataView(VentasPermisoMixin, FormView):
    template_name = 'orders/produccion-next-day.html'
    form_class = FinishOrderForm
    success_url = '.'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contar_produccion(self=self,)
        context['now'] = datetime.now()
        context['produce'] = ProduceProduct.objects.total().order_by('-created')
        return context

class CerrarDato(VentasPermisoMixin, View):
    """ suma en 1 la cantidad en un carshop """

    def post(self, request, *args, **kwargs):
        print('Por cerrar el dato')
        dato = OrderDetail.objects.filter(contar= False)
        for producto in dato:
            producto.contar=True
            producto.save()
        #
        return HttpResponseRedirect(
            reverse(
                'orders_app:orders-index',kwargs={  }
            )
        )


