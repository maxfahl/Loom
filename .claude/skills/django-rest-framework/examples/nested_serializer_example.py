# examples/nested_serializer_example.py

# This file demonstrates how to handle nested relationships in Django REST Framework serializers.
# Nested serializers allow you to represent related objects directly within the parent object's serialization.

# --- myapp/models.py ---
# from django.db import models

# class Author(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)

#     def __str__(self):
#         return self.name

# class Book(models.Model):
#     title = models.CharField(max_length=200)
#     author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
#     publication_date = models.DateField()
#     isbn = models.CharField(max_length=13, unique=True)

#     def __str__(self):
#         return self.title

# --- myapp/serializers.py ---
from rest_framework import serializers
# from .models import Author, Book # Assuming Author and Book models are defined

# Mock data for demonstration without a real database
class MockAuthor:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

class MockBook:
    def __init__(self, id, title, author, publication_date, isbn):
        self.id = id
        self.title = title
        self.author = author # This will be a MockAuthor instance
        self.publication_date = publication_date
        self.isbn = isbn

# Read-only nested serializer for Author
class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()

# Book Serializer with nested Author
class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    author = AuthorSerializer() # Nested serializer for the ForeignKey relationship
    publication_date = serializers.DateField()
    isbn = serializers.CharField(max_length=13)

    # For write operations with nested serializers, you typically need to override create/update
    def create(self, validated_data):
        author_data = validated_data.pop('author')
        # In a real app, you'd create/get the author and then the book
        # author, created = Author.objects.get_or_create(**author_data)
        # book = Book.objects.create(author=author, **validated_data)
        # return book
        print(f"Creating book with data: {validated_data}, and author: {author_data}")
        mock_author = MockAuthor(id=100, **author_data) # Mock author creation
        mock_book = MockBook(id=200, author=mock_author, **validated_data) # Mock book creation
        return mock_book

    def update(self, instance, validated_data):
        author_data = validated_data.pop('author', {})
        # Update author fields
        # instance.author.name = author_data.get('name', instance.author.name)
        # instance.author.email = author_data.get('email', instance.author.email)
        # instance.author.save()

        # Update book fields
        # instance.title = validated_data.get('title', instance.title)
        # instance.save()
        # return instance
        print(f"Updating book {instance.id} with data: {validated_data}, and author: {author_data}")
        instance.title = validated_data.get('title', instance.title)
        instance.author.name = author_data.get('name', instance.author.name)
        return instance

# --- Example Usage (conceptual) ---

# Mock Author and Book instances
mock_author_instance = MockAuthor(id=1, name="Jane Doe", email="jane@example.com")
mock_book_instance = MockBook(id=101, title="The Great Adventure", author=mock_author_instance, publication_date="2023-01-15", isbn="978-1234567890")

# 1. Serialization (Read Operation)
print("--- Serialization Example ---")
serializer = BookSerializer(mock_book_instance)
print("Serialized Book Data:", serializer.data)
# Expected output will include author details nested within the book data.

# 2. Deserialization (Create Operation)
print("\n--- Deserialization (Create) Example ---")
create_data = {
    "title": "New Horizons",
    "author": {"name": "John Smith", "email": "john@example.com"},
    "publication_date": "2024-03-10",
    "isbn": "978-0987654321"
}
create_serializer = BookSerializer(data=create_data)
if create_serializer.is_valid():
    new_book = create_serializer.save()
    print("Created Book:", new_book.title, "by", new_book.author.name)
    print("Full Data:", create_serializer.data)
else:
    print("Errors:", create_serializer.errors)

# 3. Deserialization (Update Operation)
print("\n--- Deserialization (Update) Example ---")
update_data = {
    "title": "The Grand Journey (Revised)",
    "author": {"name": "Jane A. Doe"} # Update author's name
}
update_serializer = BookSerializer(mock_book_instance, data=update_data, partial=True)
if update_serializer.is_valid():
    updated_book = update_serializer.save()
    print("Updated Book:", updated_book.title, "by", updated_book.author.name)
    print("Full Data:", update_serializer.data)
else:
    print("Errors:", update_serializer.errors)

# --- myapp/views.py (conceptual usage) ---
# from rest_framework import generics
# from .models import Book
# from .serializers import BookSerializer

# class BookListCreateView(generics.ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

# class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
