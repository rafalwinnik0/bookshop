from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, blank=True)
    price = models.FloatField()
    description = models.TextField()
    file = models.ImageField(upload_to='uploads', blank=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, through='OrderItem')

    def __str__(self):
        return f"User: {self.user}, Books: {self.books}"


class OrderItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"Order {self.order.id}, Book: {self.book.title}, Quantity: {self.quantity}"


