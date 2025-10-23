# examples/pagination_filtering.py

# This file demonstrates how to implement pagination and filtering in Django REST Framework.
# These features are crucial for building scalable APIs that can handle large datasets efficiently.

# --- myapp/models.py ---
# from django.db import models

# class Item(models.Model):
#     name = models.CharField(max_length=100)
#     category = models.CharField(max_length=50, blank=True, null=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

# --- myapp/serializers.py ---
from rest_framework import serializers
# from .models import Item # Assuming Item model is defined

class ItemSerializer(serializers.Serializer):
    # Using a basic Serializer for demonstration
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    category = serializers.CharField(max_length=50, allow_blank=True, required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    created_at = serializers.DateTimeField(read_only=True)

# --- myapp/views.py ---
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend # Requires 'django-filter' package

# Mock Item data for demonstration without a real database
_mock_items = [
    {"id": i, "name": f"Item {i}", "category": f"Category {i % 3}", "price": f"{10.0 + i * 0.5:.2f}", "created_at": f"2023-01-{(i%20)+1:02d}T10:00:00Z"}
    for i in range(1, 51)
]

# 1. Custom Pagination Classes
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class LargeResultsSetPagination(LimitOffsetPagination):
    default_limit = 20
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100

# CursorPagination is more complex and requires an ordering field, often used for infinite scroll
# class MyCursorPagination(CursorPagination):
#     page_size = 10
#     ordering = 'created_at' # Must be a unique and consistent ordering

# 2. Item List API View with Pagination and Filtering
class ItemListView(generics.ListAPIView):
    # For a real app, this would be Item.objects.all()
    # We'll simulate queryset behavior with our mock data
    # queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = StandardResultsSetPagination # Apply pagination

    # Apply filtering backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'in_stock'] # Fields to filter by (assuming they exist on model)
    search_fields = ['name', 'description'] # Fields to search within
    ordering_fields = ['price', 'created_at', 'name'] # Fields to order by

    def get_queryset(self):
        # Simulate queryset filtering for mock data
        queryset = _mock_items

        # Apply DjangoFilterBackend (conceptual for mock data)
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = [item for item in queryset if item['category'] == category]

        # Apply SearchFilter (conceptual for mock data)
        search_query = self.request.query_params.get('search', None)
        if search_query is not None:
            queryset = [item for item in queryset if search_query.lower() in item['name'].lower() or \
                                                    (item['description'] and search_query.lower() in item['description'].lower())]

        # Apply OrderingFilter (conceptual for mock data)
        ordering = self.request.query_params.get('ordering', None)
        if ordering is not None:
            reverse = False
            if ordering.startswith('-'):
                reverse = True
                ordering = ordering[1:]
            if ordering in ['price', 'created_at', 'name']:
                queryset = sorted(queryset, key=lambda x: x.get(ordering, 0), reverse=reverse)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return generics.Response(serializer.data)

    # Helper to simulate filter_queryset and paginate_queryset for mock data
    def filter_queryset(self, queryset):
        # This method is usually handled by DRF's filter backends automatically
        # For mock data, we implement a simplified version in get_queryset
        return queryset

    def paginate_queryset(self, queryset):
        # This method is usually handled by DRF's pagination class automatically
        # For mock data, we'll manually paginate for demonstration
        if not self.pagination_class:
            return None

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, self.request, view=self)
        return page

    def get_paginated_response(self, data):
        # This method is usually handled by DRF's pagination class automatically
        paginator = self.pagination_class()
        return paginator.get_paginated_response(data)

# --- myproject/urls.py (or myapp/urls.py) ---
# from django.urls import path
# from myapp.views import ItemListView

# urlpatterns = [
#     path('api/items/', ItemListView.as_view(), name='item-list'),
# ]

# To run this example (conceptually):
# 1. Set up a Django project and an app named 'myapp'.
# 2. Define the Item model in `myapp/models.py`.
# 3. Copy the `ItemSerializer` to `myapp/serializers.py`.
# 4. Copy the `ItemListView` and pagination classes to `myapp/views.py`.
# 5. Configure `urls.py` as shown above.
# 6. Install `django-filter`: `pip install django-filter` and add 'django_filters' to INSTALLED_APPS.
# 7. Run `python manage.py makemigrations` and `python manage.py migrate`.
# 8. Run `python manage.py runserver`.
# 9. Access the API with queries:
#    - http://127.0.0.1:8000/api/items/ (paginated list)
#    - http://127.0.0.1:8000/api/items/?page=2&page_size=5
#    - http://127.0.0.1:8000/api/items/?category=Category%201
#    - http://127.0.0.1:8000/api/items/?search=Item%201
#    - http://127.0.0.1:8000/api/items/?ordering=-price
