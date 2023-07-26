

from django.http import HttpResponse
from django.shortcuts import render, redirect

from rest_framework import routers, serializers, viewsets
# Create your views here.
from .models import *
from .serializers import ecomserializer
from django.contrib.auth.hashers import check_password, make_password


def contact(request):
    return render(request, 'contact.html')


def index(request):
    category_id = 1
    if request.method == "POST":
        product_id = request.POST.get("cartid")
        remove = request.POST.get('minus')
        cart_dict = request.session.get('cart')

        if cart_dict:

            quantity = cart_dict.get(product_id)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart_dict.pop(product_id)
                    else:
                        cart_dict[product_id] = quantity - 1
                else:
                    cart_dict[product_id] = quantity + 1
            else:
                cart_dict[product_id] = 1
        else:
            cart_dict = {}
            cart_dict[product_id] = 1

        request.session['cart'] = cart_dict
        print(request.session['cart'])

    cate = Category.objects.all()
    c = {}
    for i in cate:
        c.update({i.id: i.name})
        request.session['cate_name'] = c
        category_id = request.GET.get('cate_id')

    if 'search' in request.GET:
        search = request.GET['search']
        try:
            categ = Category.objects.get(name=search)
            if categ:
                products = Product.objects.filter(category=categ.id)
        except:
            products = Product.objects.filter(product_name__icontains=search)

    elif category_id:
        products = Product.objects.filter(category=category_id)

    else:
        products = Product.objects.all()
    return render(request, 'home.html', {'cat': cate, 'pro': products})


def SignUp(request):
    if request.method == "POST":
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email_id = request.POST.get('email')
        password = request.POST.get('pwd')
        mobile = request.POST.get('mobile_no')
        gender = request.POST.get('gender')

        user_info = Registration(first_name=fname, last_name=lname,
                                 email=email_id, password=make_password(password), mobile=mobile, gender=gender)
        user_info.save()

        return HttpResponse("success")


def login(request):
    if request.method == "POST":
        error_msg = None
        email_id = request.POST.get('email')
        password = request.POST.get('psd')

        try:
            fetch_info = Registration.objects.get(email=email_id)

            if check_password(password, fetch_info.password):
                request.session['name'] = fetch_info.first_name
                request.session['email'] = fetch_info.email
                request.session['customer_id'] = fetch_info.id
                return redirect('home')
            else:
                error_msg = "Password is incorrect"
        except:
            error_msg = "Email is not registered"

        return render(request, 'home.html', {'error': error_msg})


def logout(request):
    request.session.clear()
    return redirect('home')


def cart_info(request):

    cart_items = request.session.get('cart').keys()
    filtered_product = Product.objects.filter(id__in=list(cart_items))

    return render(request, 'cart.html', {'filtered_product': filtered_product})


def checkout(request):
    if request.method == "POST":
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        customerid = request.session.get('customer_id')
        cart = request.session.get('cart')
        product = Product.objects.filter(id__in=list(cart.keys()))
        if not customerid:
            return HttpResponse("please login")

        for pro in product:
            save_order_dtls = order(
                address=address,
                mobile_no=mobile,
                product=pro,
                customer=Registration(id=customerid,),
                quantity=cart.get(str(pro.id)),
                price=pro.price
            )
            save_order_dtls.save()
        request.session['cart'] = {}

        return redirect('cartdtls')


def Order_Dtls(request):

    customerid = request.session.get('customer_id')
    fetch_order = order.objects.filter(customer=customerid)

    tp = 0
    for i in fetch_order:
        tp = tp+(i.price * i.quantity)
    return render(request, 'order.html', {'fetch_dtls': fetch_order, 'tp': tp})


class serializerview(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = ecomserializer
