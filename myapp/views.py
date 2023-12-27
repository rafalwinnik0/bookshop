from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Order, OrderItem
from .forms import UserRegistrationForm, BookForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST


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
    return render(request, 'myapp/edit_book.html', {'form': form, 'book': book})


@login_required()
@require_POST
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    order, created = Order.objects.get_or_create(user=request.user, defaults={})
    order_item, created = OrderItem.objects.get_or_create(order=order, book=book, defaults={'quantity': 1})
    if not created:
        order_item.quantity += 1
        order_item.save()

    response_data = {
        'message': 'Książka dodana do koszyka',
        'book_id': book_id,
        'quantity': order_item.quantity
    }
    return JsonResponse(response_data)


def cart(request):
    order = Order.objects.get(user=request.user)
    order_items = OrderItem.objects.filter(order=order).prefetch_related('book')


    return render(request, 'myapp/cart.html', {'order_items': order_items})


# STWORZENIE ZAMÓWIENIA

# book_instance = Book.objects.get(id=book_id)  # Pobranie konkretnej książki
# order_instance = Order.objects.get(id=order_id)  # Pobranie konkretnego zamówienia
#
# order_item = OrderItem(book=book_instance, order=order_instance, quantity=2)
# order_item.save()
