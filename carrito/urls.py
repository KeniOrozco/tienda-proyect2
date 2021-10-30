from django.urls import path
from . import views

app_name = 'carrito'

urlpatterns = [
    path('', views.CartView.as_view(), name='summary'),
    path('comprar/', views.ProductoListView.as_view(), name='product-list'),
    path('comprar/<slug>/', views.ProductoDetailView.as_view(), name='product-detail'),
    path('incrementar-cantidad/<pk>/', views.IncrementarCantidadView.as_view(), name='incrementar'),
    path('decrementar-cantidad/<pk>/', views.DecrementarCantidadView.as_view(), name='decrementar'),
    path('remover-carrito/<pk>/', views.QuitarCarritoView.as_view(), name='remove-from-cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
]