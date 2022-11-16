from django.contrib import admin
#
from .models import Product, Marca, Provider, Count, ListFinal, Subproduct

from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'barcode',
        'provider',
        'marca',
        'due_date',
        'count',
        'purchase_price',
        'sale_price',
        'anulate',
    )
    search_fields = ('name', 'barcode', )
    list_filter = ('provider', 'marca', 'anulate',)


class ProviderAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone',
        'web',
    )
    search_fields = ('name',)

class CountAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'count_product',
        'add_quit',
        'comment',
        'user',
        'created',
    )
    search_fields = ('product__name',)
    list_filter = (('created', DateRangeFilter),)

admin.site.register(Product, ProductAdmin)
#
admin.site.register(Provider, ProviderAdmin)
#
admin.site.register(Marca)
#
admin.site.register(Count,CountAdmin)
#
admin.site.register(ListFinal)
#
admin.site.register(Subproduct)

