from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Order, OrderItem, UserProfile, UserAddress
from .forms import UserRegistrationForm, BookForm, AddressForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json


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
    order, created = Order.objects.get_or_create(user=request.user, status='pending', defaults={})
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


@login_required()
def cart(request):
    if Order.objects.filter(user=request.user, status='pending').exists():
        order = Order.objects.get(user=request.user, status='pending')
        order_id = order.id
        order_items = OrderItem.objects.filter(order=order).prefetch_related('book')
        total_cost = sum(item.total_price() for item in order_items)
    else:
        order_id = 0
        total_cost = 0
        order_items = None
    return render(request, 'myapp/cart.html', {'total_cost': total_cost,
                                               'order_items': order_items,
                                               'order_id': order_id})


@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        try:
            order_item = OrderItem.objects.get(id=item_id)
            order_item.delete()
            order = Order.objects.get(user=request.user)
            total = order.total_value()
            response_data = {'success': True, 'total': total}
        except OrderItem.DoesNotExist:
            response_data = {'success': False, 'error': 'Item does not exist'}
        if not OrderItem.objects.exists():
            order = Order.objects.get(user=request.user)
            order.delete()
        return JsonResponse(response_data)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def update_quantity(request, item_id):
    if request.method == "POST":
        data = json.loads(request.body)
        new_quantity = data.get('quantity')
        item = OrderItem.objects.get(id=item_id, order__user=request.user)
        item.quantity = new_quantity
        item.save()
        order = Order.objects.get(user=request.user)
        total = order.total_value()
        return JsonResponse({'success': True,
                             'new_quantity': new_quantity,
                             'new_value': item.total_price(),
                             'total': total})
    else:
        return JsonResponse({'success': False})


@login_required()
def delivery_form(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'completed'
    order.save()
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            address = address_form.save()
            user_profile, created = UserProfile.objects.get_or_create(user=request.user, defaults={})
            user_address, created = UserAddress.objects.get_or_create(profile=user_profile, address=address, defaults={})
            user_address.save()
            order.status = 'cancelled'
            order.save()
            return redirect('index')

    form = AddressForm()
    return render(request, 'myapp/delivery_form.html', {'form': form,
                                                        'order_id': order_id,
                                                        'status': order.status})


@login_required()
def history(request):
    orders = Order.objects.filter(user=request.user, status='cancelled').prefetch_related('orderitem_set')
    return render(request, 'myapp/history.html', {'orders': orders})

@login_required()
def addresses(request):
    user_profile = UserProfile.objects.get(user=request.user)
    addresses = UserAddress.objects.filter(profile=user_profile).prefetch_related('address')
    return render(request, 'myapp/addresses.html', {'addresses': addresses})
