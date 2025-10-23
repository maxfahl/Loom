# patterns/service_layer_pattern.py

# This file demonstrates the Service Layer pattern in a Django REST Framework context.
# The Service Layer abstracts business logic away from views and serializers,
# promoting cleaner code, better testability, and improved maintainability.

# --- myapp/models.py (conceptual) ---
# from django.db import models

# class Order(models.Model):
#     user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     product_name = models.CharField(max_length=255)
#     quantity = models.IntegerField()
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=50, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order {self.id} by {self.user.username}"

# --- myapp/services.py ---
# This is where your core business logic resides.

from typing import Dict, Any, List

# Mock database operations for demonstration
_mock_orders = []
_next_order_id = 1

class OrderService:
    @staticmethod
    def create_order(user_id: int, product_name: str, quantity: int, price_per_unit: float) -> Dict[str, Any]:
        """Creates a new order and calculates total price."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if price_per_unit <= 0:
            raise ValueError("Price per unit must be positive.")

        total_price = quantity * price_per_unit
        global _next_order_id
        order_data = {
            "id": _next_order_id,
            "user_id": user_id,
            "product_name": product_name,
            "quantity": quantity,
            "total_price": f"{total_price:.2f}",
            "status": "pending",
            "created_at": "2023-10-27T15:00:00Z"
        }
        _mock_orders.append(order_data)
        _next_order_id += 1
        # In a real application: Order.objects.create(user_id=user_id, ...)
        return order_data

    @staticmethod
    def get_order_by_id(order_id: int) -> Dict[str, Any] | None:
        """Retrieves an order by its ID."""
        return next((order for order in _mock_orders if order["id"] == order_id), None)

    @staticmethod
    def update_order_status(order_id: int, new_status: str) -> Dict[str, Any] | None:
        """Updates the status of an existing order."""
        order = OrderService.get_order_by_id(order_id)
        if order:
            order["status"] = new_status
            # In a real application: order.save()
            return order
        return None

    @staticmethod
    def get_user_orders(user_id: int) -> List[Dict[str, Any]]:
        """Retrieves all orders for a given user."""
        return [order for order in _mock_orders if order["user_id"] == user_id]

# --- myapp/serializers.py ---
from rest_framework import serializers

class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    product_name = serializers.CharField(max_length=255)
    quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    status = serializers.CharField(max_length=50, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    # The create method in the serializer now delegates to the service layer
    def create(self, validated_data):
        user_id = validated_data['user_id']
        product_name = validated_data['product_name']
        quantity = validated_data['quantity']
        # Assume price_per_unit is determined by business logic, not directly from client
        price_per_unit = 50.0 # Example fixed price
        try:
            order = OrderService.create_order(user_id, product_name, quantity, price_per_unit)
            return order
        except ValueError as e:
            raise serializers.ValidationError(str(e))

# --- myapp/views.py ---
from rest_framework import viewsets, status
from rest_framework.response import Response
# from .serializers import OrderSerializer # Assuming OrderSerializer is defined
# from .services import OrderService # Assuming OrderService is defined

class OrderViewSet(viewsets.ViewSet):
    """API endpoint for managing orders."""
    # For a real app, you'd use ModelViewSet and link to a queryset and serializer_class
    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer

    def list(self, request):
        # In a real app, you'd filter by request.user.id
        user_id = request.query_params.get('user_id', None)
        if user_id:
            orders = OrderService.get_user_orders(int(user_id))
        else:
            orders = _mock_orders # Return all for demo if no user_id
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        order = OrderService.get_order_by_id(int(pk))
        if order:
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save() # This calls the serializer's create method, which uses the service
            return Response(order, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Example of a custom action that uses the service layer
    # @action(detail=True, methods=['post'])
    # def mark_shipped(self, request, pk=None):
    #     order = OrderService.update_order_status(int(pk), 'shipped')
    #     if order:
    #         serializer = OrderSerializer(order)
    #         return Response(serializer.data)
    #     return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

# --- Example Usage (conceptual) ---
# This part would typically be handled by API requests.

print("--- Service Layer Demonstration ---")

# Simulate creating an order via the service
try:
    order1 = OrderService.create_order(user_id=1, product_name="Widget A", quantity=2, price_per_unit=10.0)
    print("Created Order 1:", order1)
except ValueError as e:
    print("Error creating order:", e)

try:
    order2 = OrderService.create_order(user_id=1, product_name="Gadget B", quantity=1, price_per_unit=25.5)
    print("Created Order 2:", order2)
except ValueError as e:
    print("Error creating order:", e)

# Simulate getting an order
retrieved_order = OrderService.get_order_by_id(1)
print("Retrieved Order 1:", retrieved_order)

# Simulate updating an order status
updated_order = OrderService.update_order_status(1, "shipped")
print("Updated Order 1 status:", updated_order["status"] if updated_order else "Not Found")

# Simulate getting all user orders
user_orders = OrderService.get_user_orders(1)
print("User 1 Orders:", user_orders)

# --- Benefits of Service Layer ---
# 1. Separation of Concerns: Business logic is decoupled from HTTP concerns (views) and data representation (serializers).
# 2. Testability: Service methods can be unit tested independently without needing to mock HTTP requests or serializers.
# 3. Reusability: Business logic can be reused across different views, management commands, or background tasks.
# 4. Maintainability: Changes to business rules are localized to the service layer.
