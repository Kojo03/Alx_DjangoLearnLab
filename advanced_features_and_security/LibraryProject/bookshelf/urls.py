from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('exception/', views.raise_exception, name='raise_exception'),
    path('books_placeholder/', views.books, name='books'),
    path('form/', views.form_example_view, name='form_example'),
]
