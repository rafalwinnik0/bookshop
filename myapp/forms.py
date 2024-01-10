from django import forms
from django.contrib.auth.models import User
from .models import Book, Address


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'price', 'description', 'author', 'file']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'address', 'zip_code', 'country']

