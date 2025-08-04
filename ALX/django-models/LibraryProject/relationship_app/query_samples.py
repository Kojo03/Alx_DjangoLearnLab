from relationship_app.models import Author, Library, Librarian
# List all books by a specific author
Author.objects.get(name=author_name)
Books.objects.filter(author=author)


# List all books in a library 
Library.objects.get(name=library_name)
library.books.all()


# Retrieve the librarian for a library 
library = Library.objects.get(name=library_name) 
Librarian.objects.get(library=library)
