# examples/basic_crud_api.py

# This file demonstrates a basic CRUD API using Django REST Framework's ModelViewSet and Serializers.
# It assumes a Django project with an app named 'myapp'.

# --- myapp/models.py ---
# from django.db import models

# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True, null=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     in_stock = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

# --- myapp/serializers.py ---
from rest_framework import serializers
# from .models import Product # Assuming Product model is defined

class ProductSerializer(serializers.Serializer):
    # For demonstration, using a basic Serializer. In a real app, ModelSerializer is preferred.
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_blank=True, required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    in_stock = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        # This would typically create a Product instance
        # For example: return Product.objects.create(**validated_data)
        print(f"Creating product with data: {validated_data}")
        return validated_data # Return validated data for demonstration

    def update(self, instance, validated_data):
        # This would typically update a Product instance
        # For example: 
        # instance.name = validated_data.get('name', instance.name)
        # instance.save()
        # return instance
        print(f"Updating instance {instance} with data: {validated_data}")
        updated_instance = {**instance, **validated_data}
        return updated_instance # Return updated data for demonstration

# --- myapp/views.py ---
from rest_framework import viewsets, status
from rest_framework.response import Response
# from .models import Product # Assuming Product model is defined
# from .serializers import ProductSerializer # Assuming ProductSerializer is defined

# Mock Product data for demonstration without a real database
_mock_products = [
    {"id": 1, "name": "Laptop", "description": "Powerful laptop", "price": "1200.00", "in_stock": True, "created_at": "2023-01-01T10:00:00Z"},
    {"id": 2, "name": "Mouse", "description": "Wireless mouse", "price": "25.50", "in_stock": True, "created_at": "2023-01-02T11:00:00Z"},
]
_next_id = 3

class ProductViewSet(viewsets.ViewSet):
    """A simple ViewSet for listing, retrieving, creating, updating and deleting products."""
    # For a real application, you would use ModelViewSet and link to a queryset and serializer_class
    # queryset = Product.objects.all()
    # serializer_class = ProductSerializer

    def list(self, request):
        serializer = ProductSerializer(_mock_products, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        product = next((p for p in _mock_products if p["id"] == int(pk)), None)
        if product:
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            global _next_id
            new_product = {**serializer.validated_data, "id": _next_id, "created_at": "2023-10-27T12:00:00Z"} # Mock creation
            _mock_products.append(new_product)
            _next_id += 1
            return Response(new_product, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        product_id = int(pk)
        product_index = next((i for i, p in enumerate(_mock_products) if p["id"] == product_id), -1)
        if product_index != -1:
            product = _mock_products[product_index]
            serializer = ProductSerializer(product, data=request.data, partial=False) # partial=True for PATCH
            if serializer.is_valid():
                updated_product = serializer.save() # This calls the serializer's update method
                _mock_products[product_index] = updated_product # Update mock list
                return Response(updated_product)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        product_id = int(pk)
        product_index = next((i for i, p in enumerate(_mock_products) if p["id"] == product_id), -1)
        if product_index != -1:
            product = _mock_products[product_index]
            serializer = ProductSerializer(product, data=request.data, partial=True) # partial=True for PATCH
            if serializer.is_valid():
                updated_product = serializer.save() # This calls the serializer's update method
                _mock_products[product_index] = updated_product # Update mock list
                return Response(updated_product)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        product_id = int(pk)
        global _mock_products
        initial_len = len(_mock_products)
        _mock_products = [p for p in _mock_products if p["id"] != product_id]
        if len(_mock_products) < initial_len:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

# --- myproject/urls.py (or myapp/urls.py) ---
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from myapp.views import ProductViewSet

# router = DefaultRouter()
# router.register(r'products', ProductViewSet, basename='product')

# urlpatterns = [
#     path('api/', include(router.urls)),
# ]

# To run this example (conceptually):
# 1. Set up a Django project and an app named 'myapp'.
# 2. Define the Product model in `myapp/models.py`.
# 3. Copy the `ProductSerializer` to `myapp/serializers.py`.
# 4. Copy the `ProductViewSet` to `myapp/views.py`.
# 5. Configure `urls.py` as shown above.
# 6. Run `python manage.py makemigrations` and `python manage.py migrate`.
# 7. Run `python manage.py runserver`.
# 8. Access the API at http://127.0.0.1:8000/api/products/
