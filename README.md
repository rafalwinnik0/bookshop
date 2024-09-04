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
```bash
  git clone https://github.com/rafalwinnik0/bookshop.git
```
3. Install the required dependencies:
```bash
  pip install -r requirements.txt
```
5. Apply migrations:
```bash
   python manage.py migrate
```
6. Create superuser:
```bash
  python manage.py createsuperuser
```
8. Run the development sercer:
```bash
  python manage.py runserver
```

## Project Structure	

1. models.py: Contains the Django models for the application
2. views.py: Contains the views for the application
3. urls.py: Contains the URL configurations for the application
4. tests.py: Contains the unit tests for the models

## Running Tests

To run the unit tests, use the following command:

```bash
  python manage.py test myapp
```
