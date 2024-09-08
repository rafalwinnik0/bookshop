import unittest

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Book, Order, OrderItem, Address, UserProfile, UserAddress

class BookModelTest(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            price=10.99,
            description="A test book",
            file=None
        )

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, "Test Author")
        self.assertEqual(self.book.price, 10.99)
        self.assertEqual(self.book.description, "A test book")

    def test_book_str_method(self):
        self.assertEqual(str(self.book), "Test Book")


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.book1 = Book.objects.create(title="Test Book 1", price=20.00)
        self.book2 = Book.objects.create(title="Test Book 2", price=30.00)
        self.order = Order.objects.create(user=self.user, status='pending')
        OrderItem.objects.create(order=self.order, book=self.book1, quantity=2)
        OrderItem.objects.create(order=self.order, book=self.book2, quantity=1)

    def test_order_creation(self):
        self.assertEqual(self.order.user.username, "testuser")
        self.assertEqual(self.order.status, "pending")

    def test_order_str_method(self):
        self.assertEqual(str(self.order), f"User: {self.user}, Books: {self.order.books}")

    def test_total_value(self):
        self.assertEqual(self.order.total_value(), 70.00)


class OrderItemModelTest(TestCase):

    def setUp(self):
        self.book = Book.objects.create(title="Test Book", price=15.00)
        self.user = User.objects.create(username="testuser")
        self.order = Order.objects.create(user=self.user)
        self.order_item = OrderItem.objects.create(order=self.order, book=self.book, quantity=3)

    def test_order_item_creation(self):
        self.assertEqual(self.order_item.book.title, "Test Book")
        self.assertEqual(self.order_item.quantity, 3)

    def test_order_item_str_method(self):
        self.assertEqual(str(self.order_item), f"Order {self.order.id}, Book: {self.book.title}, Quantity: 3")

    def test_total_price(self):
        self.assertEqual(self.order_item.total_price(), 45.00)


class AddressModelTest(TestCase):

    def setUp(self):
        self.address = Address.objects.create(
            first_name="John",
            last_name="Doe",
            address="123 Main St",
            zip_code="12345",
            country="USA"
        )

    def test_address_creation(self):
        self.assertEqual(self.address.first_name, "John")
        self.assertEqual(self.address.last_name, "Doe")
        self.assertEqual(self.address.address, "123 Main St")
        self.assertEqual(self.address.zip_code, "12345")
        self.assertEqual(self.address.country, "USA")


class UserProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.address = Address.objects.create(
            first_name="John",
            last_name="Doe",
            address="123 Main St",
            zip_code="12345",
            country="USA"
        )
        UserAddress.objects.create(profile=self.user_profile, address=self.address)

    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.user.username, "testuser")

    def test_user_address_creation(self):
        self.assertEqual(self.user_profile.addresses.count(), 1)
        self.assertEqual(self.user_profile.addresses.first(), self.address)