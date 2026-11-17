def carrito_info(request):
    carrito = request.session.get('carrito', {})
    return {
        'carrito_total_items': sum(int(i.get('cantidad', 0)) for i in carrito.values()),
        'carrito_total_productos': len(carrito),
    }