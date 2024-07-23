from .models import Cart


def total(request):
    u = request.user
    count = 0

    if request.user.is_authenticated:
        try:
            item = Cart.objects.filter(user=u)
            count = item.count()
        except:
            count = 0
    return {'count': count}
