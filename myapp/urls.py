from django.conf import settings
from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name='index'),
    path("register/", views.register, name='register'),
    path("login/", auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path("logout/", auth_views.LogoutView.as_view(template_name='myapp/logout.html'), name='logout'),
    path('addbook/', views.add_book, name='add_book'),
    path('editbook/<int:book_id>/', views.edit_book, name='edit_book'),
    path('<int:book_id>/', views.show_book, name='show_book'),
    path('author/<slug:author>/', views.author_site, name='author_site'),
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('delivery-form/<int:order_id>/', views.delivery_form, name='delivery_form'),
    path('history/', views.history, name='history'),
    path('addresses/', views.addresses, name='addresses'),
    path('fill-address/', views.fill_address, name='fill_address'),
    path('account/', views.account, name='account'),
    path('remove-address/<int:address_id>/', views.remove_address, name='remove_address'),
    path('update-address/', views.update_address, name='update_address'),
    path('edit-account-data/', views.edit_account_data, name='edit_account_data'),
    path('update-account/', views.update_account, name='update_account'),
    path('account-locked/', views.account_locked, name='account_locked'),
    path('search/', views.search_in_database, name='search_in_database'),
    path('search-based-on-filter/', views.search_based_on_filter, name='search_based_on_filter'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
