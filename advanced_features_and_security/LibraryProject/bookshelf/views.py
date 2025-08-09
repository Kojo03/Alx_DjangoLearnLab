from django.shortcuts import render
from .models import Book
from .forms import ExampleForm
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

# Create your views here.

def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

def raise_exception(request):
    raise PermissionDenied

def books(request):
    return HttpResponse("This is the books view.")
