from django import forms
from .models import OrdenItem, Producto, Direccion
from django.contrib.auth import get_user_model

User = get_user_model()

class AddToCartForm(forms.ModelForm):

    cantidad = forms.IntegerField(min_value=1)

    class Meta:
        model = OrdenItem
        fields = ['cantidad', ]

    def __init__(self, *args, **kwargs):
        self.producto_id = kwargs.pop('producto_id')
        producto = Producto.objects.get(id=self.producto_id)
        super().__init__(*args, **kwargs)

    def clean(self):
        producto_id = self.producto_id
        producto = Producto.objects.get(id=self.producto_id)
        cantidad = self.cleaned_data['cantidad']

        if producto.stock < cantidad:
            raise forms.ValidationError(f"La cantidad seleccionada debe ser menor {producto.stock}")




class DireccionForm(forms.Form):
    departamento = forms.CharField(required=True)
    telefono = forms.CharField(required=True, max_length=9)
    direccion = forms.CharField(required=True)
    referencia = forms.CharField(required=True)
    zipcode = forms.CharField(required=True)
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        super().__init__(*args, **kwargs)

        user = User.objects.get(id=user_id) 

