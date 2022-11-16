"""
Proyecto Final
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('', include('applications.home.urls')),
    # users app
    re_path('', include('applications.users.urls')),
    # producto app
    re_path('', include('applications.producto.urls')),
    # venta app
    re_path('', include('applications.venta.urls')),
    # caja app
    re_path('', include('applications.caja.urls')),
    # caja team
    re_path('', include('applications.team.urls')),
    re_path('', include('applications.orders.urls')),

    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
