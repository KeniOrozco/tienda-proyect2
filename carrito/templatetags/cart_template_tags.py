from django import template
from carrito.utils import get_or_set_order_session


register = template.Library()

@register.filter
def cart_item_count(request):
    orden = get_or_set_order_session(request)
    count = orden.items.count()
    return count