from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password']