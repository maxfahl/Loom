---
Name: django-rest-framework
Version: 1.0.0
Category: Backend Development / Python
Tags: Django, DRF, REST API, Python, web development, serializers, viewsets, authentication
Description: Building robust, scalable, and secure REST APIs with Django REST Framework.
---

# Django REST Framework (DRF) Skill

## 1. Skill Purpose

This skill enables Claude to effectively design, implement, and optimize RESTful APIs using Django REST Framework. It focuses on leveraging DRF's powerful features for serialization, view handling, authentication, permissions, and performance, ensuring the creation of scalable, secure, and maintainable APIs.

## 2. When to Activate This Skill

Activate this skill when:
- Developing new RESTful APIs or extending existing ones in a Django project.
- Designing data serialization and deserialization logic for API endpoints.
- Implementing authentication and authorization mechanisms for API access.
- Optimizing API performance and query efficiency.
- Performing code reviews on DRF-based API implementations.
- Discussing best practices for API development in the Django ecosystem.

## 3. Core Knowledge

The fundamental concepts, patterns, and APIs Claude needs to know regarding Django REST Framework:

### Core DRF Components:

-   **Serializers**: Convert complex data types (Django models) to native Python datatypes that can be easily rendered into JSON, XML, or other content types. Also handle deserialization and validation.
    -   `Serializer`, `ModelSerializer`
    -   `ListSerializer`, `HyperlinkedModelSerializer`
    -   `SerializerMethodField`, `PrimaryKeyRelatedField`, `SlugRelatedField`
    -   Custom fields and validators.
-   **Views**: Handle incoming HTTP requests and return HTTP responses.
    -   `APIView`: Basic building block for class-based views.
    -   `GenericAPIView`: Provides core functionality for common view behaviors.
    -   `mixins`: Reusable classes for common CRUD operations (e.g., `ListModelMixin`, `CreateModelMixin`).
    -   `generics`: Pre-built generic views combining `GenericAPIView` and mixins (e.g., `ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`).
    -   `ViewSet`: Combines the logic for a set of related views into a single class (e.g., `ViewSet`, `ModelViewSet`, `ReadOnlyModelViewSet`).
-   **Routers**: Automatically generate URL patterns for ViewSets.
    -   `SimpleRouter`, `DefaultRouter`.
-   **Authentication**: Determine the credentials of the incoming request.
    -   `TokenAuthentication`, `SessionAuthentication`, `BasicAuthentication`, `RemoteUserAuthentication`.
    -   Custom authentication classes.
-   **Permissions**: Determine if the authenticated user has permission to perform the requested action.
    -   `AllowAny`, `IsAuthenticated`, `IsAdminUser`, `IsAuthenticatedOrReadOnly`.
    -   `DjangoModelPermissions`, `DjangoObjectPermissions`.
    -   Custom permission classes.
-   **Pagination**: Control how large result sets are broken into individual pages.
    -   `PageNumberPagination`, `LimitOffsetPagination`, `CursorPagination`.
-   **Filtering**: Allow clients to filter the list of items returned by an API.
    -   `DjangoFilterBackend`, `SearchFilter`, `OrderingFilter`.
-   **Throttling**: Control the rate of requests that clients can make to an API.
    -   `AnonRateThrottle`, `UserRateThrottle`.

### Best Practices & Concepts:

-   **Modular Project Structure**: Separate concerns into distinct Django apps.
-   **Query Optimization**: Use `select_related`, `prefetch_related`, `.only()`, `.defer()` to prevent N+1 queries.
-   **Consistent Error Handling**: Provide clear and standardized error responses.
-   **API Documentation**: Use tools like drf-spectacular (OpenAPI/Swagger) for automatic documentation.
-   **Testing**: Write comprehensive tests for serializers, views, and custom components.
-   **Security**: Implement robust authentication, permissions, rate limiting, and protect sensitive data.
-   **Performance**: Caching, async views (Django 5.x), avoiding deep nesting in serializers.

## 4. Key Guidance for Claude

### Always Recommend (✅ best practices)

-   ✅ Use `ModelSerializer` for most model-backed serializers, explicitly listing `fields` or `exclude`.
-   ✅ Prefer `ModelViewSet` with `DefaultRouter` for standard CRUD operations to reduce boilerplate.
-   ✅ Implement robust authentication (e.g., JWT, Token) and permission classes (`IsAuthenticated`, custom permissions) for all API endpoints.
-   ✅ Optimize database queries using `select_related` for ForeignKey/OneToOne and `prefetch_related` for ManyToMany/reverse ForeignKey relationships.
-   ✅ Implement pagination for any list endpoint that might return a large number of objects.
-   ✅ Provide clear, consistent, and informative error responses following a standardized format.
-   ✅ Document API endpoints using `drf-spectacular` or similar tools for OpenAPI/Swagger generation.
-   ✅ Write unit and integration tests for serializers, views, and custom components.
-   ✅ Keep serializers thin; move complex business logic to model methods, managers, or service layers.
-   ✅ Use `SerializerMethodField` sparingly and optimize its underlying logic to avoid performance bottlenecks.

### Never Recommend (❌ anti-patterns)

-   ❌ Never expose all model fields by default in `ModelSerializer` using `fields = '__all__'`, especially for sensitive data.
-   ❌ Avoid deep nesting of serializers unless absolutely necessary, as it can lead to N+1 query problems and large payloads.
-   ❌ Do not put complex business logic directly into `views.py` or `serializers.py`; abstract it into separate service or utility modules.
-   ❌ Never use `AllowAny` as a default permission class in production APIs without careful consideration.
-   ❌ Avoid making unnecessary database queries within serializer methods or view logic.
-   ❌ Do not hardcode credentials or sensitive configuration directly in settings files; use environment variables.
-   ❌ Never run a production API with `DEBUG = True`.
-   ❌ Avoid returning generic HTTP 500 errors without providing specific, actionable error details to the client.

### Common Questions & Responses (FAQ format)

**Q: How do I handle nested relationships in DRF?**
A: For read-only nested data, use nested serializers. For writeable nested data, consider using `PrimaryKeyRelatedField` or `SlugRelatedField` for simplicity, or implement custom `create()` and `update()` methods in your serializer for more complex nested write operations. Avoid deep writeable nesting as it can become complex.

**Q: My API is slow. How can I improve performance?**
A: Start by identifying bottlenecks. Use `select_related` and `prefetch_related` in your `queryset` to reduce database queries. Optimize serializer fields, avoiding `SerializerMethodField` if its logic is expensive. Implement pagination. Consider caching strategies (e.g., view caching, per-object caching). Profile your API to pinpoint exact slow points.

**Q: How do I implement custom permissions in DRF?**
A: Create a class that inherits from `rest_framework.permissions.BasePermission`. Override `has_permission(self, request, view)` for object-level permissions or `has_object_permission(self, request, view, obj)` for object-level permissions. Return `True` or `False` based on your logic. Add your custom permission class to `permission_classes` in your view.

**Q: What's the best way to structure a large DRF project?**
A: Follow Django's app structure, where each app represents a distinct feature or domain. Keep models, serializers, views, and tests within their respective apps. Use a `services.py` or `managers.py` file within each app for business logic. Centralize common utilities, authentication, and permissions in a dedicated `core` or `common` app.

## 5. Anti-Patterns to Flag

### Example 1: Exposing All Fields in Serializer

**BAD:**
```python
# users/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' # Exposes all fields, including potentially sensitive ones like password hash
```
*Problem*: This can inadvertently expose sensitive data (e.g., password hashes, internal flags) or unnecessary fields, leading to security vulnerabilities or bloated API responses.

**GOOD:**
```python
# users/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name'] # Explicitly list allowed fields
        read_only_fields = ['username'] # Mark fields that should not be updated via API
```
*Solution*: Always explicitly list the fields you want to expose. Use `read_only_fields` for fields that should not be modifiable by the client.

### Example 2: N+1 Query Problem in Views

**BAD:**
```python
# products/views.py
from rest_framework import generics
from .models import Product, Category
from .serializers import ProductSerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# products/serializers.py
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category_name']
```
*Problem*: For each `Product` in the queryset, accessing `product.category.name` will trigger a separate database query to fetch the `Category` object, leading to N+1 queries (1 for products, N for categories).

**GOOD:**
```python
# products/views.py
from rest_framework import generics
from .models import Product, Category
from .serializers import ProductSerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.select_related('category').all() # Use select_related to fetch category in one query
    serializer_class = ProductSerializer

# products/serializers.py (same as above)
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category_name']
```
*Solution*: Use `select_related()` for ForeignKey relationships to fetch related objects in the same query, avoiding the N+1 problem.

## 6. Code Review Checklist

-   [ ] Are serializers explicitly defining `fields` or `exclude`?
-   [ ] Is `ModelViewSet` used for standard CRUD operations where appropriate?
-   [ ] Are authentication and permission classes correctly applied to views?
-   [ ] Are database queries optimized using `select_related` and `prefetch_related`?
-   [ ] Is pagination implemented for list endpoints?
-   [ ] Are error responses consistent and informative?
-   [ ] Is API documentation generated (e.g., via `drf-spectacular`)?
-   [ ] Are serializers kept thin, with business logic abstracted elsewhere?
-   [ ] Are sensitive fields excluded from serializers?
-   [ ] Are custom permissions implemented correctly for fine-grained access control?
-   [ ] Is the project configured for security best practices (e.g., `DEBUG=False` in production, environment variables for secrets)?

## 7. Related Skills

-   `rest-api-design`: General principles for designing effective RESTful APIs.
-   `api-error-responses`: Specific guidance on standardizing API error handling.
-   `python-type-hints`: Applying type hints in Django/DRF code for better maintainability.
-   `tdd-red-green-refactor`: Writing tests for DRF components.

## 8. Examples Directory Structure

```
django-rest-framework/
├── examples/
│   ├── basic_crud_api.py           # Simple ModelViewSet and Serializer
│   ├── custom_permission_example.py # Custom permission class usage
│   ├── nested_serializer_example.py # Handling nested data with serializers
│   └── pagination_filtering.py      # Implementing pagination and filtering
├── patterns/
│   ├── service_layer_pattern.py    # Abstracting business logic from views/serializers
│   └── custom_throttling.py        # Implementing custom rate limiting
├── scripts/
│   ├── drf-project-init.sh         # Shell script to initialize Django+DRF project
│   ├── drf-app-generator.py        # Python script to generate DRF app boilerplate
│   ├── drf-permission-generator.py # Python script to generate custom permission classes
│   └── drf-serializer-validator.py # Python script to analyze DRF serializers
└── README.md
```

## 9. Custom Scripts Section

Here are 4 automation scripts designed to save significant time when working with Django REST Framework:

1.  **`drf-project-init.sh`**: Initializes a new Django project, installs Django REST Framework, and sets up basic DRF configurations in `settings.py` and `urls.py`.
2.  **`drf-app-generator.py`**: A Python script that generates a new Django app with boilerplate DRF components, including a model, serializer, viewset, and basic URL configuration, based on user input.
3.  **`drf-permission-generator.py`**: A Python script to generate a custom DRF permission class template, guiding the user through defining object-level or global permissions.
4.  **`drf-serializer-validator.py`**: A Python script that analyzes DRF serializer files for common anti-patterns, such as `fields = '__all__'` or potential N+1 query issues in `SerializerMethodField` usage, providing warnings and suggestions.
