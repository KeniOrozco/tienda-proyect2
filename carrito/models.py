from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.shortcuts import reverse

#modelo de usuario
Usuario = get_user_model()


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nombre

class Direccion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='direc')
    telefono = models.CharField(max_length=8)
    departamento = models.CharField(max_length=50)
    direccion = models.CharField(max_length=150) 
    referencia = models.CharField(max_length=150) 
    zipcode = models.CharField(max_length=6) 
    default = models.BooleanField(default=False) 
    
    def __str__(self):
        return f"{self.referencia}"

    class Meta:
        verbose_name_plural = 'Direccion'


class Producto(models.Model):
    titulo = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200, unique=True)
    imagen = models.ImageField(upload_to='producto_imagen')
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=9, decimal_places=2)
    activo = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categoria, related_name='categoria', on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("cart:product-detail", kwargs={'slug': self.slug})

    def get_price(self):
        return "{:.2f}".format(self.precio)

    @property
    def in_stock(self):
        return self.stock > 11


class OrdenItem(models.Model):
    orden = models.ForeignKey("Orden", related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default = 1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.titulo}"

    def get_raw_total_item_price(self):
        return self.cantidad * self.producto.precio

    def get_total_item_price(self):
        precio = self.get_raw_total_item_price() #1000
        return "{:.2f}".format(precio)


    class Meta:
        verbose_name_plural = 'Orden de items'

TRASPORTE= ( 
    (0, 'FORZA'), 
    (1, 'GUATEX'), 
    (2, 'CARGO'),
) 

class Orden(models.Model):
    usuario = models.ForeignKey(
        Usuario,blank=True, null=True, on_delete=models.CASCADE, related_name='orden_user')
    inicio_orden = models.DateTimeField(auto_now_add=True)
    fecha_orden = models.DateTimeField(blank=True, null=True)
    ordenada = models.BooleanField(default=False)
    estado_pago = models.BooleanField(default=False)
    no_guia = models.CharField(max_length=50)
    trasporte = models.IntegerField(choices=TRASPORTE, default=0)
    direccion_entrega = models.ForeignKey(
        Direccion, related_name='orden_entrega', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
            txt="{0} {1} {2} {3} {4}"
            return txt.format(self.numero_referencia, self.fecha_orden, self.direccion, self.telefono, self.user.name )
    
    def __str__(self):
        return self.numero_referencia

    @property
    def numero_referencia(self):
        return f"ORDEN-{self.pk}"

    def get_raw_subtotal(self):
        total = 0
        for orden_item in self.items.all():
            total += orden_item.get_raw_total_item_price()
        return total

    def get_subtotal(self):
        subtotal = self.get_raw_subtotal()
        return "{:.2f}".format(subtotal)

    def get_raw_total(self):
        subtotal = self.get_raw_subtotal()
        # agregar suma de IGV, Delivery, Resta DESCUENTOS
        #total = subtotal - discounts + tax + delivery
        return subtotal

    def get_total(self):
        total = self.get_raw_total()
        return "{:.2f}".format(total)

    class Meta:
        verbose_name_plural = 'Orden'

