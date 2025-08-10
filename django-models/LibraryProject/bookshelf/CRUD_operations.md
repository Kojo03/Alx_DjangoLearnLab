from bookshelf.models import Book

book = Book.objects.create(title = "1984", author = "George Orwell", publication_year = 1949)

print(book)

# Output : 1984 by George Orwell (1949)


retrieved_book.title = "Nineteen Eighty-Four"
retrieved_book.save()

updated_book = Book.objects.get(id=retrieved_book.id)
print(updated_book.title)

# Output : Nineteen Eighty-Four


retrieved_book = Book.objects.get(title="1984") 

print(retrieved_book.title, retrieved_book.author, retrieved_book.publication_year)

# Output : 1984 George Orwell 1949


from bookshelf.models import Book

updated_book.delete()
 
books = Book.objects.all() 

print(list(books))

# Output : [] 