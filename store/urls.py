from django.urls import path
from.views import *


urlpatterns=[
    path('',home,name='home'),
    path('product/',product,name='product'),
    path('search/',search,name='search'),
    path('products/<str:id>',product_details,name='product_details'),
    path('contactus/',contactus,name='contactus'),
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),

    #CART SESSION
    path('cart/add/<int:id>/',cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/',item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',item_decrement, name='item_decrement'),
    path('cart/cart_clear/',cart_clear, name='cart_clear'),
    path('cart/cart-detail/',cart_detail,name='cart_detail'),
    path('cart/checkout/',checkout,name='checkout'),
    path('placeorder/',place_order,name='placeorder'),
    path('success/',success,name='success'),
    path('order/',order,name='order'),
]