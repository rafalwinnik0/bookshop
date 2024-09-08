from django import forms
from django.contrib.auth.models import User
from .models import Book, Address

from django_recaptcha.fields import ReCaptchaField

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password']

    captcha = ReCaptchaField()

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'price', 'description', 'author', 'file']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'address', 'zip_code', 'country']

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'id': 'firstName'})
        self.fields['last_name'].widget.attrs.update({'id': 'lastName'})
        self.fields['address'].widget.attrs.update({'id': 'address'})
        self.fields['zip_code'].widget.attrs.update({'id': 'zipCode'})
        self.fields['country'].widget.attrs.update({'id': 'country'})

