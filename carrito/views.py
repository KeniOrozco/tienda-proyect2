import datetime
import json
from django.views import generic
from django.db.models import Q
from .utils import get_or_set_order_session
from .models import Producto, OrdenItem, Direccion, Orden, Categoria
from .forms import AddToCartForm, DireccionForm
from django.shortcuts import get_object_or_404, reverse, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
#Lista todos los productos
class ProductoListView(generic.ListView):
    template_name='cart/producto_list.html'
    paginate_by = 10 #paginacion de productos 
    def get_queryset(self):
        qs = Producto.objects.all()
        categoria = self.request.GET.get('categoria', None)
        if categoria:
            qs = qs.filter(Q(categoria__nombre=categoria))
        return qs

    def get_context_data(self, **kwargs):
        context = super(ProductoListView, self).get_context_data(**kwargs)
        context.update({
            "categorias": Categoria.objects.all()
        })
        return context
#Retorna el detalle de los productos
class ProductoDetailView(generic.FormView):
    template_name = 'cart/producto_detalle.html'
    form_class = AddToCartForm
    def get_object(self):
        return get_object_or_404(Producto, slug=self.kwargs["slug"])

    def get_success_url(self):
        return reverse("cart:summary")

    def get_form_kwargs(self):
        kwargs = super(ProductoDetailView, self).get_form_kwargs()
        kwargs["producto_id"] = self.get_object().id
        return kwargs

    def form_valid(self, form):
        orden = get_or_set_order_session(self.request)
        producto = self.get_object()
        item_filter = orden.items.filter(
            producto=producto,
        )

        if item_filter.exists():
            item = item_filter.first()
            item.cantidad  += int(form.cleaned_data['cantidad'])
            item.save()

        else:
            new_item = form.save(commit=False)
            new_item.producto = producto
            new_item.orden = orden
            new_item.save()
        return super(ProductoDetailView, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(ProductoDetailView, self).get_context_data(**kwargs)
        context['producto'] = self.get_object()
        return context


class CartView(generic.TemplateView):
    template_name = 'cart/carrito.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context["orden"] = get_or_set_order_session(self.request)
        return context


class IncrementarCantidadView(generic.View):
    def get(self, request, *args, **kwargs):
        orden_item = get_object_or_404(OrdenItem, id=kwargs['pk'])
        orden_item.cantidad += 1
        orden_item.save()
        return redirect("cart:summary")


class DecrementarCantidadView(generic.View):
    def get(self, request, *args, **kwargs):
        orden_item = get_object_or_404(OrdenItem, id=kwargs['pk'])
        if orden_item.cantidad <= 1:
            orden_item.delete()
        else:
            orden_item.cantidad  -= 1
            orden_item.save()
        return redirect("cart:summary")


class QuitarCarritoView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrdenItem, id=kwargs['pk'])
        order_item.delete()
        return redirect("cart:summary")


class CheckoutView(generic.FormView):
    template_name = 'cart/checkout.html'
    form_class = DireccionForm

    def get_success_url(self):
        return reverse("cart:summary")

    def form_valid(self, form):
        orden = get_or_set_order_session(self.request)
        direccion = Direccion.objects.create(

            usuario = self.request.user,
            departamento =form.cleaned_data['departamento'],
            telefono =form.cleaned_data['telefono'],
            direccion =form.cleaned_data['direccion'],
            referencia =form.cleaned_data['referencia'],
            zipcode =form.cleaned_data['zipcode'],
        )
        orden.direccion_entrega = direccion #pasa el id de la direccion a orden
        orden.fecha_orden = datetime.datetime.now()
        orden.ordenada = True
        orden.save()
        messages.info(
            self.request, "Se han agegador tus productos espera nuestra llamada para la confirmacion")
        return super(CheckoutView, self).form_valid(form)
        
    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context['orden'] = get_or_set_order_session(self.request)
        return context



 

