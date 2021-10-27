from django.contrib import admin
from .models import (
    Producto, 
    Orden, 
    OrdenItem, 
    Direccion,
    Categoria
)
admin.site.register(Producto)
admin.site.register(Direccion)
admin.site.register(Orden)
admin.site.register(OrdenItem)
admin.site.register(Categoria)