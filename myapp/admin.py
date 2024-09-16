from django.contrib import admin
from .models import Book, Order, OrderItem, Address, Genre

admin.site.register(Book)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Genre)
