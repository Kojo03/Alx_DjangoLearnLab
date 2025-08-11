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

def form_example_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return HttpResponse("Form submitted successfully!")
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})
