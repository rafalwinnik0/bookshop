from django.shortcuts import render
from .models import Book
from .forms import UserRegistrationForm
from django.views.decorators.csrf import csrf_protect
# @csrf_protect

def index(request):
    books = Book.objects.all()
    return render(request, 'myapp/index.html', {'books':books})

def modal_site(request):
    return render(request, 'myapp/modal_site.html')
def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.save()
    user_form = UserRegistrationForm()
    return render(request, 'myapp/register.html', {'user_form':user_form})