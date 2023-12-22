from django.shortcuts import render, get_object_or_404
from .models import Book
from .forms import UserRegistrationForm, BookForm


def index(request):
    books = Book.objects.all()
    adam_mickiewicz_books = Book.objects.filter(author='Adam-Mickiewicz')
    return render(request,
                  'myapp/index.html',
                  {'books': books, 'Adam_Mickiewicz_books': adam_mickiewicz_books})


def modal_site(request):
    return render(request, 'myapp/modal_site.html')


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.save()
    user_form = UserRegistrationForm()
    return render(request, 'myapp/register.html', {'user_form': user_form})


def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()

            if not request.FILES.get('file'):
                book.file = 'static/book_icon.png'

            book.save()

    form = BookForm()
    return render(request, 'myapp/add_book.html', {'form': form})


def show_book(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'myapp/show_book.html', {'book': book})


def author_site(request, author):
    books = Book.objects.filter(author=author)
    return render(request, 'myapp/author_site.html', {'books': books, 'author': author})


def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
    else:
        form = BookForm(instance=book)
    return render(request, 'myapp/edit_book.html', {'form': form, 'book':book})