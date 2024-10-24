from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Book, Order, OrderItem, UserProfile, UserAddress, Address
from .forms import UserRegistrationForm, BookForm, AddressForm

from itertools import zip_longest
import json


def group_books(books, n):
    args = [iter(books)] * n
    return zip_longest(*args)


def index(request):
    books = Book.objects.all().order_by('title')
    grouped_books = group_books(books, 8)
    return render(request, 'myapp/index.html', {'grouped_books': grouped_books})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')

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
    paginator = Paginator(books, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'myapp/author_site.html', {'page_obj': page_obj, 'author': author})


def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
    else:
        form = BookForm(instance=book)
    return render(request, 'myapp/edit_book.html', {'form': form, 'book': book})


@login_required
def update_address(request):
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')

        try:
            addr = Address.objects.get(id=address_id)
            addr.first_name = first_name
            addr.last_name = last_name
            addr.address = address
            addr.zip_code = zip_code
            addr.country = country
            addr.save()
            return JsonResponse({'success': True,
                                 'zip_code': zip_code,
                                 'address': address,
                                 'country': country,
                                 'address_id': address_id})
        except Address.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Address not found'})


@login_required
def update_account(request):
    if request.method == 'POST':
        new_first_name = request.POST.get('new_first_name')
        new_last_name = request.POST.get('new_last_name')
        new_username = request.POST.get('new_username')
        new_email = request.POST.get('new_email')
        user = User.objects.get(username=request.user.username)
        user.username = new_username
        user.email = new_email
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.save()
        response = {'success': True}
    else:
        response = {'success': False}
    return JsonResponse(response)


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
            order = Order.objects.get(user=request.user, status='pending')
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
def remove_address(request, address_id):
    try:
        address = Address.objects.get(id=address_id)
        user_address = UserAddress.objects.get(address=address)
        address.delete()
        user_address.delete()
        response_data = {'success': True}
    except (UserAddress.DoesNotExist, Address.DoesNotExist):
        response_data = {'success': False}
    return JsonResponse(response_data)


@login_required
def update_quantity(request, item_id):
    if request.method == "POST":
        data = json.loads(request.body)
        new_quantity = data.get('quantity')
        item = OrderItem.objects.get(id=item_id, order__user=request.user)
        item.quantity = new_quantity
        item.save()
        order = Order.objects.get(user=request.user, status='pending')
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
            address_data = address_form.cleaned_data
            address, address_created = Address.objects.get_or_create(
                first_name=address_data['first_name'],
                last_name=address_data['last_name'],
                address=address_data['address'],
                zip_code=address_data['zip_code'],
                country=address_data['country']
            )
            user_profile, profile_created = UserProfile.objects.get_or_create(user=request.user)
            user_address, user_address_created = UserAddress.objects.get_or_create(profile=user_profile,
                                                                                   address=address)
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
    user_profile, profile_created = UserProfile.objects.get_or_create(user=request.user)
    addresses = UserAddress.objects.filter(profile=user_profile).prefetch_related('address')
    return render(request, 'myapp/addresses.html', {'addresses': addresses})


@login_required()
def fill_address(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile:
        user_address = UserAddress.objects.filter(profile=user_profile).first()
        if user_address is None:
            response = {'success': True,
                        'first_name': '',
                        'last_name': '',
                        'address': '',
                        'zip_code': '',
                        'country': '',
                        }
        else:
            response = {'success': True,
                        'first_name': user_address.address.first_name,
                        'last_name': user_address.address.last_name,
                        'address': user_address.address.address,
                        'zip_code': user_address.address.zip_code,
                        'country': user_address.address.country,
                        }
    else:
        response = {'success': False}

    return JsonResponse(response)


@login_required()
def account(request):
    user_addresses = UserProfile.objects.filter(user=request.user).prefetch_related('useraddress_set')
    user_orders = Order.objects.filter(user=request.user, status='cancelled').prefetch_related('orderitem_set')
    return render(request, 'myapp/account.html', {'user_addresses': user_addresses, 'user_orders': user_orders})


@login_required()
def edit_account_data(request):
    pass


def account_locked(request):
    return render(request, 'myapp/account-locked.html')


def search_in_database(request):
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(title__startswith=query)
        books_data = list(books.values('id', 'title', 'author', 'price', 'file'))
        return JsonResponse(books_data, safe=False)
    return JsonResponse([], safe=False)


def search_based_on_filter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        filters = Q()
        checked_author = data.get('authorCheckedValues', [])
        checked_category = data.get('categoryCheckedValues', [])
        selectedSorting = data.get('selectedSorting', 'Sortowanie')
        min_range = data.get('minRange', None)
        max_range = data.get('maxRange', None)
        if min_range:
            filters &= Q(price__gte=int(min_range))
            print(f"added min_range: {min_range}")
        if max_range:
            filters &= Q(price__lte=int(max_range))
            print(f"added max_range: {max_range}")
        if checked_author:
            filters &= Q(author__in=checked_author)
            print(f"added author: {checked_author}")
        if checked_category:
            filters &= Q(genres__name__in=checked_category)
            print(f"added category: {checked_category}")

        books = Book.objects.filter(filters).distinct()

        if selectedSorting != '':
            if selectedSorting == 'title_asc':
                books = books.order_by('title')
            elif selectedSorting == 'title_desc':
                books = books.order_by('-title')
            elif selectedSorting == 'price_asc':
                books = books.order_by('price')
            else:
                books = books.order_by('-price')
        else:
            pass

        books_data = []
        for book in books:
            books_data.append({
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'price': book.price,
                'file': book.file.url if book.file else ''
            })

        paginator_f = Paginator(books_data, 8)
        page_number = request.GET.get('page')
        page_obj = paginator_f.get_page(page_number)
        return JsonResponse({
            'success': True,
            'books': list(page_obj),
            'page_obj': {
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
                'num_pages': paginator_f.num_pages,
                'page_number': page_obj.number,
                'page_range': list(paginator_f.page_range),
            }
        })


def category(request):
    books = Book.objects.all().order_by('title')
    paginator = Paginator(books, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,
                  'myapp/category.html',
                  {'page_obj': page_obj})


def new_filter(request):
    # Receive data from fetch api
    # data = json.loads(request.body)
    # author_filters = data.get('authors', [])
    # category_filters = data.get('categories', [])
    # min_range = data.get('minRange', None)
    # max_range = data.get('maxRange', None)

    author_filters = request.GET.getlist('author')
    category_filters = request.GET.getlist('category')
    min_range = request.GET.get('minRange', None)
    max_range = request.GET.get('maxRange', None)
    sorting_method = request.GET.get('selected_sorting', None)

    filters = Q()

    if author_filters:
        filters &= Q(author__in=author_filters)
    if category_filters:
        filters &= Q(genres__name__in=category_filters)
    if min_range:
        filters &= Q(price__gte=float(min_range))
    if max_range:
        filters &= Q(price__lte=float(max_range))

    books = Book.objects.filter(filters).distinct()

    if sorting_method != 'default':
        if sorting_method == 'title_asc':
            books = books.order_by('title')
        elif sorting_method == 'title_desc':
            books = books.order_by('-title')
        elif sorting_method == 'price_asc':
            books = books.order_by('price')
        else:
            books = books.order_by('-price')
    else:
        books = books.order_by('title')

    paginator = Paginator(books, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'myapp/filter.html', {'page_obj': page_obj,
                                                 'sorting_method': sorting_method})


def for_men(request):
    return render(request, 'myapp/bestsellers_for_men.html')


def premieres(request):
    return render(request, 'myapp/premieres.html')


def relation_books(request):
    return render(request, 'myapp/relation_books.html')

