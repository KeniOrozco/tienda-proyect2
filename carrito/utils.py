from .models import Orden


def get_or_set_order_session(request):
    orden_id = request.session.get('orden_id', None)
    if orden_id is None:
        orden = Orden()
        orden.save()
        request.session['orden_id'] = orden.id

    else: 
        try:
            orden = Orden.objects.get(id=orden_id, ordenada=False)
        except Orden.DoesNotExist:
            orden = Orden()
            orden.save()
            request.session['orden_id'] = orden.id

    if request.user.is_authenticated and orden.usuario is None:
        orden.usuario= request.user
        orden.save()
    return orden

