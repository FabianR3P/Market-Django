from django import forms
#local
from django.contrib.admin import widgets
import time
import datetime
from datetime import date
from datetime import datetime

class OrderForm(forms.Form):
    barcode = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Codigo de barras',
                'class': 'form-control',
                'id' : 'resultado',
            }
        )
    )
    count = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(
            attrs = {
                'value': '0',
                'class': 'form-control',
                  'id' : 'result',
            }        )
    )
    comen = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Pan',
                'name' : 'comen.name',
                'class': 'form-control',
                'id' : 'type',
            }
        )
    )

    def clean_count(self):
        count = self.cleaned_data['count']
        if count < 1:
            raise forms.ValidationError('Ingrese una cantidad mayor a cero')

        return count

class DetailOrderForm(forms.Form):
    pay_ammount = forms.DecimalField(
        min_value=0,
        widget=forms.NumberInput(
            attrs = {
                'value': '0',
                'class': 'form-control',
                'id' : 'result',
                }
            )
    )

    date_order = forms.DateField(
        widget=forms.DateInput(
            format = '%Y-%m-%d',
            attrs = {
            'type' : 'date',
            'class': 'form-control',
            'id' : 'resultDay'
            }
        )
    )

    hour_order = forms.TimeField(
        initial=time.strftime('%H:%M:%S', time.localtime()),
        widget=forms.DateInput(
            attrs = {
            'type' : '',
            'class': 'form-control',
            'id' : 'resultdate',
            }
        )
    )

    ruta = forms.CharField(
        widget=forms.Select(
            attrs = {
            'type' : 'select',
            'class': 'form-control',
            }
        )
    )
    finish = forms.CharField(
        required=False,
        widget=forms.Select(
            attrs = {
            'type' : 'select',
            'class': 'form-control',
            'value': 'false'
            }
        )
    )


    def clean_count(self,**kwargs):
        total = OrderCarShop.objects.total_cobrar(id_client)
        pay_ammount = self.cleaned_data['pay_ammount']
        if pay_ammount > total:
            raise forms.ValidationError('Ingrese una cantidad menor al total o seleccione la opcion de pagado')

        return count

class FinishOrderForm(forms.Form):
    pay = forms.DecimalField(
        min_value=0,
        widget=forms.NumberInput(
            attrs = {
                'value': '0',
                'class': 'form-control',
                'id' : 'result',
                }
            )
    )
