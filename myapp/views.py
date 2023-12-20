from django.shortcuts import render
from .models import Book
from .forms import UserRegistrationForm, NewBookForm
from django.views.decorators.csrf import csrf_protect
# @csrf_protect

def index(request):
    books = Book.objects.all()
    Adam_Mickiewicz_books = Book.objects.filter(author='Adam-Mickiewicz')
    return render(request, 'myapp/index.html', {'books':books,'Adam_Mickiewicz_books':Adam_Mickiewicz_books})

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

def add_book(request):
    if request.method == "POST":
        form = NewBookForm(request.POST, request.FILES)
        if form.is_valid():
            new_book = form.save()

    form = NewBookForm()
    return render(request, 'myapp/add_book.html', {'form':form})

def edit_book(request):
    return render(request, 'myapp/edit_book.html')

def show_book(request, id):
    book = Book.objects.get(id=id)
    return render(request, 'myapp/show_book.html', {'book':book})

def author_site(request, author):
    print(author)
    books = Book.objects.filter(author=author)
    return render(request, 'myapp/author_site.html', {'books':books, 'author':author})