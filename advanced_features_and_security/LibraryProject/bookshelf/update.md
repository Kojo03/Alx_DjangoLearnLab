retrieved_book.title = "Nineteen Eighty-Four"
retrieved_book.save()

updated_book = Book.objects.get(id=retrieved_book.id)
print(updated_book.title)

# Output : Nineteen Eighty-Four