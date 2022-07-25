from binascii import rledecode_hqx
from http import client
from multiprocessing import context
from multiprocessing.connection import Client
import re
from turtle import pos
from django.http import HttpResponse
from django.shortcuts import redirect, render
from requests import post
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as Login,logout as Logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import razorpay
from django.views.decorators.csrf import csrf_exempt

# Razorpay

client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))


# Create your views here.


def home(request):
    product=Product.objects.filter(status='Publish')
    context={
        'product':product
    }


    return render(request,'store/index.html',context)

def product(request):
    categories=Categories.objects.all()
    filterprice=FilterPrice.objects.all()
    color=Color.objects.all()
    brand=Brand.objects.all()

    catID=request.GET.get('categories')
    priceID=request.GET.get('filter_price')
    colorID=request.GET.get('color')
    brandID=request.GET.get('brand')
    priceLID=request.GET.get('priceL')
    priceHID=request.GET.get('priceH')
    newPID=request.GET.get('newP')
    oldPID=request.GET.get('oldP')
    if catID:
        product=Product.objects.filter(categories=catID,status='Publish')
    elif priceID:
        product=Product.objects.filter(filter_price=priceID,status='Publish')
    elif colorID:
        product=Product.objects.filter(color=colorID,status='Publish')
    elif brandID:
        product=Product.objects.filter(brand=brandID,status='Publish')
    elif priceLID:
        product=Product.objects.filter(status='Publish').order_by('price')
    elif priceHID:
        product=Product.objects.filter(status='Publish').order_by('-price')
    elif newPID:
        product=Product.objects.filter(status='Publish',condition='New').order_by('-id')
    elif oldPID:
        product=Product.objects.filter(status='Publish',condition='Old').order_by('-id')
    else:
        product=Product.objects.filter(status='Publish')

    context={
        'product':product,
        'categories':categories,
        'filterprice':filterprice,
        'color':color,
        'brand':brand,
    }

    return render(request,'store/product.html',context)


def search(request):
    query=request.GET.get('query')
    product=Product.objects.filter(name__icontains=query)
    context={
        'product':product,

    }

    return render(request,'store/search.html',context)


def product_details(request,id):
    prod=Product.objects.filter(id=id).first()

    context={
        'prod':prod
    }
    return render(request,'store/product_details.html',context)


def contactus(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        contactus=ContactUs(name=name,email=email,subject=subject,message=message)
        
        
        subject=subject
        message=message
        email_from=settings.EMAIL_HOST_USER 
        recipient_list = [contactus.email, ]

        try:
            send_mail(subject,message,email_from,recipient_list)
            contactus.save()
            return redirect(home)
        except:
            return redirect(contactus)

    return render(request,'store/contactus.html')


def register(request):
    if request.method=='POST':
        username=request.POST.get('username')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        email=request.POST.get('email')
        password=request.POST.get('password1')
        # password2=request.POST.get('password2')

        customer=User.objects.create_user(username,email,password)
        customer.first_name=firstname
        customer.last_name=lastname
        customer.save()

        return redirect(login)

    return render(request,'store/auth.html')


def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user=authenticate(username=username,password=password)

        if user is not None:
            Login(request, user)
            return redirect(home)
        else:
            return redirect(login)


    return render(request,'store/auth.html')



def logout(request):
    Logout(request)
    return redirect(home)






@login_required(login_url="login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_detail(request):
    return render(request, 'store/cart.html')


@login_required(login_url="login")
def checkout(request):
    amount=request.POST.get('amount')
    amountf=float(amount)
    int_amount=int(amountf)
    
    payment=client.order.create(
        {
            "amount": int_amount,
            "currency": "INR",
            'payment_capture':1,
        }
    )

    order_id=payment['id']
    context={
        'order_id':order_id,
        'payment':payment,
        'amount':amount,
    }
    return render(request,'store/checkout.html',context)


@login_required(login_url="login")
def place_order(request):
    if request.method=='POST':
        uid=request.session.get('_auth_user_id')
        user=User.objects.get(id=uid)
        cart=request.session.get('cart')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        order_id=request.POST.get('order_id')
        payment=request.POST.get('payment')
        country=request.POST.get('country')
        address=request.POST.get('address')
        city=request.POST.get('city')
        state=request.POST.get('state')
        postcode=request.POST.get('postcode')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        amount=request.POST.get('amount')

        order_id=request.POST.get('order_id')
        payment=request.POST.get('payment')

        context={
            'order_id':order_id,
        }

        order=Order(
            user=user,
            firstname=firstname,
            lastname=lastname,
            payment_id=order_id,
            country=country,
            address=address,
            city=city,
            state=state,
            postcode=postcode,
            phone=phone,
            email=email,
            amount=amount,
        )
        order.save()
        for i in cart:
            p=(int(cart[i]['price']))
            q=cart[i]['quantity']

            total=p * q
            print(total)
            
            item=OrderItem(
                user=user,
                order=order,
                product=cart[i]['name'],
                image=cart[i]['image'],
                quantity=cart[i]['quantity'],
                price=cart[i]['price'],
                total=total
            )
            item.save()
        return render(request,'store/placeorder.html',context)


@csrf_exempt
def success(request):
    if request.method=='POST':
        a=request.POST
        order_id=""
        for key, val in a.items():
            if key=='razorpay_order_id':
                order_id=val
                break

        user=Order.objects.filter(payment_id=order_id).first()
        user.paid=True
        user.save()
        Cart(request).clear()

    return render(request,'store/thankyou.html')


@login_required(login_url="login")
def order(request):

    uid=request.session.get('_auth_user_id')
    user=User.objects.get(id=uid)

    order=OrderItem.objects.filter(user=user)
    context={
        'order':order
    }
    return render(request,'store/order.html',context)

