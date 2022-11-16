from django.contrib import admin
from .models import Client, ProductByClient,Order ,Ruta, OrderDetail,OrderCarShop

# Register your models here.
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'nickname',
        'name',
        'f_name',
    )
    search_fields = ('nickname',)

    def __str__(self):
        return self.name



class ProductByClientAdmin(admin.ModelAdmin):
    list_display = (
        'client',
        'product',
        'price',
    )
    search_fields = ('client',)
    def __str__(self):
        return self.client.name




admin.site.register(Client,ClientAdmin)

admin.site.register(ProductByClient,ProductByClientAdmin)

admin.site.register(Order)

admin.site.register(Ruta)

admin.site.register(OrderDetail)

admin.site.register(OrderCarShop)
