# django
from django import forms
# local
from .models import Product, Count, ListFinal

class CountForm(forms.ModelForm):

    class Meta:
        """Form para registrar agregar productos."""
        model = Count
        fields = (
        'count_product',
        #'add_quit',
        'comment',
        'user_produce',
        )
        widgets = {
            'count_product': forms.TextInput(
                attrs = {
                    'placeholder': 'Cantidad a modificar',
                    'type' : 'text',
                    'class': 'use-keyboard-input form-control',
                    'aria-describedby' : 'basic-addon1',
                    'id' : 'result',
                }
            ),
            'comment': forms.Select(
                attrs = {
                    'class': 'form-select form-select-lg ',
                }
            ),
            'user_produce': forms.Select(
                attrs = {
                    'class': 'form-select',
                }
            ),

        }
        
class ReportForm(forms.Form):

    class Meta:
        """Form para registrar agregar productos."""

        widgets = {
            'count_product': forms.TextInput(
                attrs = {
                    'placeholder': 'Cantidad amodificar',
                    'class': 'use-keyboard-input input-group-field',
                }
            ),
            'user_produce': forms.Select(
                attrs = {
                    'class': 'input-group-field',
                }
            ),
            'comment': forms.Select(
                attrs = {
                    'class': 'input-group-field',
                }
            ),

        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'barcode',
            'name',
            'provider',
            'marca',
            'due_date',
            'description',
            'unit',
            'count',
            'purchase_price',
            'sale_price',
            'sale_price1',
            'sale_price2',
            'sale_price3',
            'sale_price4',
            'percent',
            'sale_last',

        )
        widgets = {
            'barcode': forms.TextInput(
                attrs = {
                    'autocomplete' : 'off',
                    'placeholder': 'Codigo de barras',
                    'class': 'use-keyboard-input input-group-field',
                }
            ),
            'name': forms.TextInput(
                attrs = {
                    'placeholder': 'Nombre...',
                    'class': 'use-keyboard-input input-group-field',
                }
            ),
            'due_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'type': 'date',
                    'class': 'input-group-field',
                }
            ),
            'description': forms.Textarea(
                attrs = {
                    'placeholder': 'Descripcion del producto',
                    'rows': '3',
                    'class': 'use-keyboard-input input-group-field',
                }
            ),
            'unit': forms.Select(
                attrs = {
                    'class': 'input-group-field',
                }
            ),
            'count': forms.TextInput(
                attrs = {
                    'placeholder': 'Cantidad en almacen',
                    'class': 'use-keyboard-input input-group-field  botonenviar ',
                    'id' : 'addinput',
                    'name' : 'addinput'
                }
            ),
            'purchase_price': forms.TextInput(
                attrs = {
                    'placeholder': '1',
                    'class': 'use-keyboard-input input-group-field',
                }
            ),
            'sale_price': forms.TextInput(
                attrs = {
                    'placeholder': '1',
                    'class': 'use-keyboard-input input-group-field',
                }
            ),
            'sale_price1': forms.TextInput(
                attrs = {
                    'placeholder': 'precio 2',
                    'class': 'use-keyboard-input input-group-field',
                }
            ),
            'sale_price2': forms.TextInput(
                attrs = {
                    'placeholder': 'precio 2',
                    'class': 'use-keyboard-input input-group-field',
                }
            ),
            'sale_price3': forms.TextInput(
                attrs = {
                    'placeholder': 'precio 3',
                    'class': 'use-keyboard-input input-group-field',
                }
            ),
            'sale_price4': forms.TextInput(
                attrs = {
                    'placeholder': 'precio 4',
                    'class': 'use-keyboard-input input-group-field',
                }
            ),
             'percent': forms.TextInput(
                
                attrs = {
                    'placeholder': 'porcentaje ganancia',
                    'class': 'use-keyboard-input input-group-field',
                }
            ),
            'sale_last': forms.TextInput(
                attrs = {
                    'placeholder': 'precio  pan frio',
                    'class': 'use-keyboard-input input-group-field',
                }
            ),
        }
    # validations
    def clean_barcode(self):
        barcode = self.cleaned_data['barcode']
        if len(barcode) < 2:
            raise forms.ValidationError('Ingrese un codigo de barras correcto')

        return barcode

    def clean_purchase_price(self):
        purchase_price = self.cleaned_data['purchase_price']
        if not purchase_price > 0:
            raise forms.ValidationError('Ingrese un precio compra mayor a cero')

        return purchase_price

    def clean_sale_price(self):
        sale_price = self.cleaned_data['sale_price']
        purchase_price = self.cleaned_data.get('purchase_price')
        if not sale_price >= purchase_price:
            raise forms.ValidationError('El precio de venta debe ser mayor o igual que el precio de compra')

        return sale_price

class ReportProductForm(forms.Form):
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
            min_value=0,
            widget=forms.NumberInput(
                attrs = {
                    'value': '',
                    'class': 'form-control',
                      'id' : 'result',
                }
            )
        )
