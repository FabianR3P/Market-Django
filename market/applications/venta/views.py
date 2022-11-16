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

from applications.producto.models import Product
from applications.utils import render_to_pdf
from applications.users.mixins import VentasPermisoMixin
from django.contrib import messages

#
from .models import Sale, SaleDetail, CarShop
from .forms import VentaForm, VentaVoucherForm
from .functions import procesar_venta

from django.contrib import messages

#
from django.contrib.auth.models import User


class AddCarView(VentasPermisoMixin, FormView):
    template_name = 'venta/index.html'
    form_class = VentaForm
    success_url = '.'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car_num = self.kwargs['car_num']
        context["productos"] = CarShop.objects.filter(user = self.request.user, number_shop=car_num)
        id = self.kwargs['id']
        context["car_num"] = self.kwargs['car_num']
        #price = self.kwargs['price']
        context["total_cobrar"] = CarShop.objects.total_cobrar(id,car_num)
        # formulario para venta con voucher
        context['form_voucher'] = VentaVoucherForm
        #print("Entra a la data")
        return context


    def form_valid(self, form,*args, **kwargs):
        #obtener id de usuario
        id_user = self.kwargs['id']
        car_num = self.kwargs['car_num']
        barcode = form.cleaned_data['barcode']
        count = form.cleaned_data['count']
        price = form.cleaned_data['price']
        check = Product.objects.get(barcode=barcode)
        if price == 1:
            sub_total = check.sale_price * count

        elif price == 2:
            if check.sale_price2 == 0 or check.sale_price2== None:
                sub_total=0
            else:
                print(check.sale_price2)
                sub_total = check.sale_price2 * count

        elif price == 3:
            if check.sale_price3 == 0 or check.sale_price3== None:
                sub_total=0
            else:
                print(check.sale_price3)
                sub_total = check.sale_price3 * count

        elif price == 4:
            if check.sale_price4 == 0 or check.sale_price4 == None:
                sub_total=0
            else:
                print(check.sale_price4)
                sub_total = check.sale_price4 * count
        elif price == 5:
            if check.sale_price1 == 0 or check.sale_price1== None:
                sub_total=0
            else:
                print(check.sale_price1)
                sub_total = check.sale_price1 * count
                
        elif price == 6:
            if check.sale_last == 0 or check.sale_last == None:
                sub_total=0
            else:
                print(check.sale_last)
                sub_total = check.sale_last * count

        if check.count >= count:
            print("Tienes stock")
            obj, created = CarShop.objects.get_or_create(
                barcode=barcode,
                user=self.request.user,
                number_shop= car_num,
                defaults={
                    'product': Product.objects.get(barcode=barcode),
                    'count': count,
                    'price': price,
                    'sub_total' : sub_total,

                }
            )
            #
            if not created and price == obj.price:
                obj.count = obj.count + count
                obj.sub_total = obj.sub_total + sub_total
                if obj.count < check.count:
                    obj.save()
            super(AddCarView, self).form_valid(form)
            return HttpResponseRedirect(
                reverse(
                    'venta_app:venta-index',kwargs={ "id":id_user,"car_num":car_num}
                )
            )
        else:
            print("No tienes stock"+ check.name)
            messages.warning(self.request,check.name)
            return HttpResponseRedirect(
                reverse(
                    'venta_app:venta-index',kwargs={ "id":id_user,"car_num":car_num}
                )
            )

class CarShopUpdateView(VentasPermisoMixin, View):
    """ quita en 1 la cantidad en un carshop """

    def sample_view(request):
        current_user = request.user
        print("IMPRESIONES DEL ID")
        print (current_user.id)

    def post(self, request, *args, **kwargs):
        id_user = self.kwargs['id_user']
        car_num = self.kwargs['car_num']
        car = CarShop.objects.get(id=self.kwargs['pk'], number_shop=car_num)
        print(car)
        if car.count > 1:
            car.count = car.count - 1
            print("comprobando subtotal")
            producto = Product.objects.get(barcode=car.barcode)
            if car.price == 1:
                precio = producto.sale_price

            elif car.price == 2:
                precio = producto.sale_price2

            elif car.price == 3:
                precio = producto.sale_price3

            elif car.price == 4:
                precio = producto.sale_price4

            elif car.price == 5:
                precio = producto.sale_price1
                
            elif car.price == 6:
                precio = producto.sale_last

            car.sub_total = precio * car.count
            print(car.count)
            print(car.price)
            print(car.sub_total)
            print(precio)
            car.save()
        #
        return HttpResponseRedirect(
            reverse(
                'venta_app:venta-index',kwargs={ "id":id_user,"car_num":car_num }
            )
        )

class CarShopUpdatePlusView(VentasPermisoMixin, View):
    """ suma en 1 la cantidad en un carshop """

    def post(self, request, *args, **kwargs):
        id_user = self.kwargs['id_user']
        car_num = self.kwargs['car_num']
        car = CarShop.objects.get(id=self.kwargs['pk'], number_shop=car_num)
        check = Product.objects.get(barcode=car.barcode)
        if car.count > 0 and car.count<check.count:
            car.count = car.count + 1
            producto = Product.objects.get(barcode=car.barcode)
            if car.price == 1:
                precio = producto.sale_price

            elif car.price == 2:
                precio = producto.sale_price2

            elif car.price == 3:
                precio = producto.sale_price3

            elif car.price == 4:
                precio = producto.sale_price4

            elif car.price == 5:
                precio = producto.sale_price1
                
            elif car.price == 6:
                precio = producto.sale_last
                
            car.sub_total = precio * car.count
            car.save()
        #
            return HttpResponseRedirect(
                reverse(
                    'venta_app:venta-index',kwargs={ "id": id_user, "car_num": car_num }
                )
            )
        
        else:
                print("No tienes stock"+ check.name)
                messages.warning(self.request, check.name)
                return HttpResponseRedirect(
                    reverse(
                        'venta_app:venta-index',kwargs={ "id":id_user,"car_num":car_num}
                    )
            )

class CarShopDeleteView(VentasPermisoMixin, View):
    model = CarShop
    def post(self, request, *args, **kwargs):
        CarShop.objects.filter(id=self.kwargs['pk']).delete()
        id_user = self.kwargs['id_user']
        car_num = self.kwargs['car_num']
        return HttpResponseRedirect(
            reverse(
                'venta_app:venta-index',kwargs={ "id": id_user, "car_num": car_num}
            )
        )


class CarShopDeleteAll(VentasPermisoMixin, View):

    def post(self, request, *args, **kwargs):
        id_user = self.kwargs['id_user']
        car = self.kwargs['car_num']

        CarShop.objects.filter(user = self.request.user).delete()
        #
        return HttpResponseRedirect(
            reverse(

                'venta_app:venta-index',kwargs={ "id": id_user, "car_num": car }

            )
        )


class ProcesoVentaSimpleView(VentasPermisoMixin, View):
    """ Procesa una venta simple """

    def post(self, request, *args, **kwargs):
        #
        id_user = self.kwargs['id_user']
        car = self.kwargs['car_num']

        procesar_venta(
            self=self,
            type_invoce=Sale.SIN_COMPROBANTE,
            type_payment=Sale.CASH,
            user=self.request.user,

        )
        #
        return HttpResponseRedirect(
            reverse(
                'venta_app:venta-index',kwargs={ "id": id_user, "car_num": car }
            )
        )

class ProcesoVentaVoucherView(VentasPermisoMixin, FormView):
    form_class = VentaVoucherForm
    success_url = '.'

    def form_valid(self, form):
        type_payment = form.cleaned_data['type_payment']
        type_invoce = form.cleaned_data['type_invoce']
        #
        venta = procesar_venta(
            self=self,
            type_invoce=type_invoce,
            type_payment=type_payment,
            user=self.request.user,
        )
        #
        if venta:
            return HttpResponseRedirect(
                reverse(
                    'venta_app:venta-voucher_pdf',
                    kwargs={'pk': venta.pk },
                )
            )
        else:
            return HttpResponseRedirect(
                reverse(
                #    'venta_app:venta-index'
                )
            )

class VentaVoucherPdf(VentasPermisoMixin, View):

    def get(self, request, *args, **kwargs):
        venta = Sale.objects.get(id=self.kwargs['pk'])
        data = {
            'venta': venta,
            'detalle_productos': SaleDetail.objects.filter(sale__id=self.kwargs['pk'])
        }
        pdf = render_to_pdf('venta/voucher.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

class SaleListView(VentasPermisoMixin, ListView):
    template_name = 'venta/ventasB.html'
    context_object_name = "ventas"
    paginate_by = 30

    def get_queryset(self):
        id_user = self.kwargs['id_user']
        return Sale.objects.ventas_no_cerradas(id_user).order_by("-id")



class SaleDeleteView(VentasPermisoMixin, DeleteView):
    template_name = "venta/delete.html"
    model = Sale
    #success_url = reverse_lazy('venta_app:venta-index')

    def delete(self, request, *args, **kwargs):
        #id_user = self.kwargs['id_user']
        self.object = self.get_object()
        self.object.anulate = True
        self.object.save()
        # actualizmos sl stok y ventas
        SaleDetail.objects.restablecer_stok_num_ventas(self.object.id)
        #success_url = self.get_success_url

        return HttpResponseRedirect(
            reverse(
            'home_app:index'
            )
        )

class SaleView(VentasPermisoMixin, ListView):
    template_name = 'venta/ventas-view.html'
    context_object_name = "ventas"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['venta_detail'] = Sale.objects.filter(id=pk).order_by("-id")
        context['productos'] = SaleDetail.objects.filter(sale_id=pk).order_by("-id")

        print( context['productos'] )
        return context

    def get_queryset(self):
        pk = self.kwargs['pk']
        return SaleDetail.objects.filter(sale_id=pk).order_by("-id")
