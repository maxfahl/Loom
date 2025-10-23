# examples/custom_permission_example.py

# This file demonstrates how to implement custom permission classes in Django REST Framework.
# Custom permissions allow fine-grained control over who can access certain API endpoints or objects.

# --- myapp/permissions.py ---
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Read-only access is allowed for authenticated users.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    Read-only access is allowed for any authenticated user.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any authenticated user.
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # Write permissions are only allowed to admin users.
        return request.user and request.user.is_staff

# --- myapp/views.py (example usage) ---
from rest_framework import generics
# from .models import Product # Assuming Product model is defined
# from .serializers import ProductSerializer # Assuming ProductSerializer is defined
# from .permissions import IsOwnerOrReadOnly, IsAdminUserOrReadOnly # Assuming permissions are defined

# Mock Product data and User for demonstration
class MockUser:
    def __init__(self, username, is_authenticated=True, is_staff=False):
        self.username = username
        self.is_authenticated = is_authenticated
        self.is_staff = is_staff

class MockProduct:
    def __init__(self, id, name, owner):
        self.id = id
        self.name = name
        self.owner = owner

# Example: Product owned by 'admin'
mock_product_1 = MockProduct(1, "Admin's Product", MockUser('admin', is_staff=True))
mock_product_2 = MockProduct(2, "User's Product", MockUser('regular_user'))

# This is a conceptual example of how you'd apply permissions to a view.
# In a real Django app, you'd use actual models and serializers.

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Product.objects.all()
    # serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly] # Apply custom permission

    def get_object(self):
        # In a real scenario, this would fetch from the database
        # For demonstration, we'll simulate fetching an object
        pk = self.kwargs.get('pk')
        if pk == '1':
            return mock_product_1
        elif pk == '2':
            return mock_product_2
        return None

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj and self.request.user.is_authenticated and self.has_object_permission(request, self, obj):
            return generics.Response({"id": obj.id, "name": obj.name, "owner": obj.owner.username})
        return generics.Response({"detail": "Not found or permission denied"}, status=403)

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj and self.request.user.is_authenticated and self.has_object_permission(request, self, obj):
            # Simulate update
            obj.name = request.data.get('name', obj.name)
            return generics.Response({"id": obj.id, "name": obj.name, "owner": obj.owner.username})
        return generics.Response({"detail": "Not found or permission denied"}, status=403)

    # Helper to simulate permission check
    def has_object_permission(self, request, view, obj):
        # Instantiate the permission class and call its method
        return IsOwnerOrReadOnly().has_object_permission(request, view, obj)

# --- Example Usage (conceptual) ---
# Simulate requests with different users

# Request by owner (admin) to edit their product
# request = MockRequest(user=MockUser('admin', is_staff=True), method='PUT', data={'name': 'Updated Admin Product'})
# view = ProductDetailView.as_view()
# response = view(request, pk='1')
# print(f"Admin editing own product: {response.status_code} {response.data}")

# Request by non-owner (regular_user) to edit another's product
# request = MockRequest(user=MockUser('regular_user'), method='PUT', data={'name': 'Updated Other Product'})
# view = ProductDetailView.as_view()
# response = view(request, pk='1')
# print(f"User editing other's product: {response.status_code} {response.data}")

# Request by non-owner (regular_user) to view another's product (read-only allowed)
# request = MockRequest(user=MockUser('regular_user'), method='GET')
# view = ProductDetailView.as_view()
# response = view(request, pk='1')
# print(f"User viewing other's product: {response.status_code} {response.data}")
