from django.conf import settings
from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name='index'),
    path("modal_site/", views.modal_site, name='modal_site'),
    path("register/", views.register, name='register'),
    path("login/", auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='myapp/logout.html'), name='logout'),
    path('addbook/', views.add_book, name='add_book'),
    path('editbook/<int:book_id>/', views.edit_book, name='edit_book'),
    path('<int:book_id>/', views.show_book, name='show_book'),
    path('author/<slug:author>/', views.author_site, name='author_site'),
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
