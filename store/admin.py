from django.contrib import admin
from .models import *

# Register your models here.

class ImageTublerinline(admin.TabularInline):
    model= Images


class TagTublerinline(admin.TabularInline):
    model=Tag


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines=[ImageTublerinline,TagTublerinline]
    list_display=[
        'name','status',
    ]

class OrderItemTublerinline(admin.TabularInline):
    model=OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderItemTublerinline]
    list_display=[
        'user','firstname','phone','email','amount','payment_id','paid','date',
    ]
    search_fields=['firstname','email','payment_id']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=[
        'user','product','price','quantity','total',
    ]




admin.site.register(Categories)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(FilterPrice)
admin.site.register(Images)
admin.site.register(Tag)
admin.site.register(ContactUs)
