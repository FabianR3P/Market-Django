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
#
from .models import Sale_team, SaleDetail, CarShop_team
from .forms import VentaForm, VentaVoucherForm
from .functions import procesar_venta
#
#from django.contrib.auth.models import User

from applications.users.models import User

class AddCarView(VentasPermisoMixin, FormView):
    template_name = 'team/index.html'
    form_class = VentaForm
    success_url = '.'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car_num = self.kwargs['car_num']
        user_team = self.kwargs['user_team']
        print(user_team)
        #Recupera productos de cada empleado sin importar la sesion del vendedor
        context["productos"] = CarShop_team.objects.filter(team_user = user_team, number_shop=car_num)
        id = self.kwargs['id']
        context["car_num"] = self.kwargs['car_num']
        #id de persona de la deuda
        context["user_team"] = self.kwargs['user_team']
        context["user_t"] = User.objects.get(id=user_team)
        #price = self.kwargs['price']
        context["total_cobrar"] = CarShop_team.objects.total_cobrar(user_team,car_num)
        # formulario para venta con voucher
        context['form_voucher'] = VentaVoucherForm
        #print("Entra a la data")
        return context

    def form_valid(self, form,*args, **kwargs):
        #obtener id de usuario
        user_team = self.kwargs['user_team']
        print(user_team)
        id_user = self.kwargs['id']
        car_num = self.kwargs['car_num']
        barcode = form.cleaned_data['barcode']
        count = form.cleaned_data['count']
        price = form.cleaned_data['price']
        created = CarShop_team.objects.create(
            barcode=barcode,
            user=self.request.user,
            team_user= User.objects.get(id=user_team),
            number_shop= car_num,
            count = count,
            product = Product.objects.get(barcode=barcode),
            price = price
            #defaults={
            #    'product': Product.objects.get(barcode=barcode),
            #    'count': count,
            #    'price': price
            #}
        )
        product =Product.objects.get(barcode=barcode)
        print(product.count)
        #axtualiza stock de lo que se consume en la pana
        product.count = product.count - count
        #se agrega el conteo de ventas de productos
        product.num_sale = product.num_sale + count

        product.save()

        #
        if not created:
            obj.count = obj.count + count
            obj.save()
        super(AddCarView, self).form_valid(form)
        return HttpResponseRedirect(
            reverse(
                'team_app:team-index',kwargs={ "id":id_user,"car_num":car_num, "user_team":user_team}
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
        user_team = self.kwargs['user_team']
        car = CarShop_team.objects.get(id=self.kwargs['pk'], number_shop=car_num)
        print(car)
        if car.count > 1:
            car.count = car.count - 1
            car.save()
        #
        return HttpResponseRedirect(
            reverse(
                'team_app:team-index',kwargs={ "id":id_user,"car_num":car_num,"user_team":user_team }
            )
        )

class CarShopUpdatePlusView(VentasPermisoMixin, View):
    """ suma en 1 la cantidad en un carshop """

    def post(self, request, *args, **kwargs):
        id_user = self.kwargs['id_user']
        car_num = self.kwargs['car_num']
        user_team = self.kwargs['user_team']
        car = CarShop_team.objects.get(id=self.kwargs['pk'], number_shop=car_num)
        if car.count > 0:
            car.count = car.count + 1
            car.save()
        #
        return HttpResponseRedirect(
            reverse(
                'team_app:team-index',kwargs={ "id": id_user, "car_num": car_num,"user_team":user_team }
            )
        )


class CarShopDeleteView(VentasPermisoMixin, View):
    model = CarShop_team
    def post(self, request, *args, **kwargs):
        CarShop_team.objects.filter(id=self.kwargs['pk']).delete()
        id_user = self.kwargs['id_user']
        user_team = self.kwargs['user_team']
        car = self.kwargs['car_num']
        return HttpResponseRedirect(
            reverse(
                'team_app:team-index',kwargs={ "id": id_user, "car_num": '0',"user_team":user_team}
            )
        )


class CarShopDeleteAll(VentasPermisoMixin, View):

    def post(self, request, *args, **kwargs):
        id_user = self.kwargs['id_user']
        car = self.kwargs['car_num']

        CarShop_team.objects.filter(user = self.request.user).delete()
        #
        return HttpResponseRedirect(
            reverse(

                'team_app:team-index',kwargs={ "id": id_user, "car_num": car }

            )
        )

class ProcesoVentaSimpleView(VentasPermisoMixin, View):
    """ Procesa una venta simple """

    def post(self, request, *args, **kwargs):
        #
        id_user = self.kwargs['id_user']
        car = self.kwargs['car_num']
        user_team = self.kwargs['user_team']
        print(user_team)
        procesar_venta(
            self=self,
            type_invoce=Sale_team.SIN_COMPROBANTE,
            type_payment=Sale_team.CASH,
            user=self.request.user,
            team_user_id=user_team,
        )
        #
        return HttpResponseRedirect(
            reverse(
                'team_app:team-index',kwargs={ "id": id_user, "car_num": car, "user_team": user_team }
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
                    'team_app:venta-voucher_pdf',
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
        venta = Sale_team.objects.get(id=self.kwargs['pk'])
        data = {
            'venta': venta,
            'detalle_productos': SaleDetail.objects.filter(sale__id=self.kwargs['pk'])
        }
        pdf = render_to_pdf('team/voucher.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

class SaleListView(VentasPermisoMixin, ListView):
    template_name = 'team/ventas.html'
    context_object_name = "ventas"

    def get_queryset(self):
        id_user = self.kwargs['id_user']
        return Sale_team.objects.ventas_no_cerradas(id_user).order_by("-id")

class SaleDeleteView(VentasPermisoMixin, DeleteView):
    template_name = "team/delete.html"
    model = Sale_team
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
