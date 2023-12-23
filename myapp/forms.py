from django import forms
from django.contrib.auth.models import User
from .models import Book


class UserRegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'price', 'description', 'author', 'file']
