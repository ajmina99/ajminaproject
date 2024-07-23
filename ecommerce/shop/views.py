from django.shortcuts import render,redirect
from shop.models import Category, Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def category(request):
    c = Category.objects.all()
    return render(request, 'category.html', {'category': c})


def all_products(request, i):
    main_cate = Category.objects.get(id=i)
    pro = Product.objects.filter(category=main_cate)
    context = {'main_cate': main_cate , 'pro': pro}
    return render(request, 'product.html', context)

def product_details(request,i):
    product=Product.objects.get(id=i)
    return render(request,'productdetails.html',{'product':product})


def register(request):
    if (request.method == "POST"):
        u = request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        fn = request.POST['f']
        ln = request.POST['l']
        e = request.POST['e']

        if (cp == p):
            user = User.objects.create_user(username=u, password=p, first_name=fn, last_name=ln, email=e)
            user.save()
            return redirect('shop:category')

    return render(request, 'register.html')

def user_login(request):
    if (request.method == "POST"):
        u = request.POST['u']
        p = request.POST['p']
        user = authenticate(username=u, password=p)
        if user:
            login(request,user)
            return redirect('shop:category')
        else:
            # return HttpResponse("Invalid Credentials")
            messages.error(request,"Invalid Credentials")
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('shop:login')