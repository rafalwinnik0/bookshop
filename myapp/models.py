from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    AKC = 'akcja'
    PRZ = 'przygoda'
    HIS = 'historia'
    KOM = 'komedia'
    BOOK_GENRE = [
        (AKC, 'Akcja'),
        (PRZ, 'Przygoda'),
        (HIS, 'Historia'),
        (KOM, 'Komedia')
    ]
    name = models.CharField(max_length=15, choices=BOOK_GENRE, default=AKC)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, blank=True)
    price = models.FloatField()
    description = models.TextField()
    file = models.ImageField(upload_to='uploads', blank=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    genres = models.ManyToManyField(Genre, blank=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, through='OrderItem')

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    def __str__(self):
        return f"User: {self.user}, Books: {self.books}"

    def total_value(self):
        return sum(book.total_price() for book in self.orderitem_set.all())


class OrderItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"Order {self.order.id}, Book: {self.book.title}, Quantity: {self.quantity}"

    def total_price(self):
        return self.quantity * self.book.price


class Address(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=15)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    addresses = models.ManyToManyField('Address', through='UserAddress')


class UserAddress(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
