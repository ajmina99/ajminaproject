import razorpay
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from razorpay import Client
from razorpay.resources import payment
from shop.models import Product
from cart.models import Cart, Payment, Order_table
from django.contrib.auth.models import User


@login_required
def add_to_cart(request, pk):
    p = Product.objects.get(id=pk)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        if (p.stock > 0):
            cart.quantity += 1
            cart.save()
            p.stock -= 1
            p.save()
    except:
        if (p.stock):
            cart = Cart.objects.create(product=p, user=u, quantity=1)
            cart.save()
            p.stock -= 1
            p.save()
    return redirect('cart:cart_view')


@login_required
def cart_view(request):
    u = request.user
    cart = Cart.objects.filter(user=u)
    total = 0
    for i in cart:
        total = total + i.quantity * i.product.price

    return render(request, 'cart.html', {'cart': cart, 'total': total})


def cart_decrement(request, p):
    p = Product.objects.get(id=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        if (cart.quantity > 1):
            cart.quantity -= 1
            cart.save()
            p.stock += 1
            p.save()
        else:
            cart.delete()
            p.stock += 1
            p.save()
    except:
        pass
    return cart_view(request)


def remove(request, p):
    p = Product.objects.get(id=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        cart.delete()
        p.stock += cart.quantity
        p.save()
    except:
        pass
    return cart_view(request)


def order_form(request):
    if (request.method == "POST"):
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        pin = request.POST.get('pin')

        u = request.user
        c = Cart.objects.filter(user=u)

        total = 0
        for i in c:
            total = total + (i.quantity * i.product.price)  # total amount
        total = int(total * 100)

        # create razorpay client using our API crendentials
        client = razorpay.Client(auth=('rzp_test_JxkEAhDs0tS7ex', 'eoQ9m3vQ1nvjJ0ZRtYTHCELJ'))

        # create order
        response_payment = client.order.create(dict(amount=total, currency="INR"))
        print(response_payment)
        order_id = response_payment['id']
        order_status = response_payment['status']
        if order_status == "created":
            p = Payment.objects.create(name=u.username, amount=total, order_id=order_id)
            p.save()
            for i in c:
                o = Order_table.objects.create(user=u, product=i.product, address=address, phone=phone, pin=pin,
                                               no_of_items=i.quantity, order_id=order_id)
                o.save()

        response_payment['name'] = u.username
        return render(request, 'payment.html', {'payment': response_payment})

    return render(request, 'orderform.html')


@csrf_exempt
def payment_status(request, u):
    print(request.user.is_authenticated)  # False
    if not request.user.is_authenticated:
        user = User.objects.get(username=u)
        login(request, user)
        print(request.user.is_authenticated)  # True

    if (request.method == "POST"):
        response = request.POST  # response after payment
        # print(response)
        # print(u)

        payment_id = response.get('razorpay_order_id')
        order_id = response.get('razorpay_order_id')
        signature = response.get('razorpay_signature')

        param_dict = {
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_signature': response['razorpay_signature']
        }
        client = razorpay.Client(auth=('rzp_test_JxkEAhDs0tS7ex', 'eoQ9m3vQ1nvjJ0ZRtYTHCELJ'))
        try:
            status = client.utility.verify_payment_signature(
                param_dict)  # to check the authenticity of razorpay signature
            print(status)

            # after successfull payment
            # retrive a payment record with particular order_id
            ord = Payment.objects.get(order_id=response['razorpay_order_id'])

            ord.razorpay_payment_id = response['razorpay_payment_id']
            ord.paid = True  # edit paid to true
            ord.save()


            u = User.objects.get(username=u)
            # print(u.username)
            c = Cart.objects.filter(user=u)
            # filter the order_table details for particular user with order_id=response['razorpay_order_id']
            o = Order_table.objects.filter(user=u, order_id=response['razorpay_order_id'])

            for i in o:
                i.payment_status = 'paid'  # edit payment status into paid
                i.save()


            c.delete()  # delete the cart items for particular user
            return render(request, 'payment_status.html', {'status': True})

        except:
            return render(request, 'payment_status.html', {'status': False})

    return render(request, 'payment_status.html')


@login_required
def order_view(request):
    u = request.user
    customer = Order_table.objects.filter(user=u, payment_status="paid")
    return render(request, 'orderview.html', {'customer': customer, 'u': u.username})
