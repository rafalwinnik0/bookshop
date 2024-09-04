# Django Bookstore Project

This Django project is a simple bookstore application that allows users to purchase books and manage their orders and addresses.

## Features

- User registration and authentication
- Book management
- Order management
- Address management

## Models

The project includes the following models:

1. **Book**: Represents a book with fields for title, author, price, description, and file upload.
2. **Order**: Represents an order with fields for the user, status, and related books.
3. **OrderItem**: Represents an item in an order, linking a book with a quantity.
4. **Address**: Represents a shipping address.
5. **UserProfile**: Represents a user profile, linking to a user and multiple addresses.

## Setup

To get started with this project:

1. Clone the repository:
  git clone https://github.com/rafalwinnik0/bookshop.git
2. Install the required dependencies:
  pip install -r requirements.txt
3. Apply migrations:
   python manage.py migrate
4. Create superuser:
  python manage.py createsuperuser
5. Run the development sercer:
  python manage.py runserver

## Project Structure	

1. models.py: Contains the Django models for the application
2. views.py: Contains the views for the application
3. urls.py: Contains the URL configurations for the application
4. tests.py: Contains the unit tests for the models
