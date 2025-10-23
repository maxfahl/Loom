# patterns/data_validation.py

# This file demonstrates using Pydantic for data validation with Python type hints.
# Pydantic is a powerful library that uses type annotations to define data schemas
# and provides runtime validation, serialization, and deserialization.

from pydantic import BaseModel, Field, EmailStr, ValidationError
from typing import List, Optional, Literal

# 1. Basic Pydantic Model
#    - Define a class that inherits from BaseModel.
#    - Use type hints to define the fields and their types.

class User(BaseModel):
    id: int
    name: str = "John Doe" # Default value
    email: EmailStr # Pydantic provides specific types like EmailStr
    is_active: bool = True
    age: Optional[int] = None # Optional field

# Example 1: Valid data
try:
    user1 = User(id=1, email="alice@example.com")
    print(f"User 1: {user1.model_dump_json(indent=2)}")
except ValidationError as e:
    print(f"Validation Error: {e}")

# Example 2: Valid data with all fields
try:
    user2 = User(id=2, name="Bob Smith", email="bob@example.com", is_active=False, age=45)
    print(f"User 2: {user2.model_dump_json(indent=2)}")
except ValidationError as e:
    print(f"Validation Error: {e}")

# Example 3: Invalid data (missing required field)
try:
    # user3 = User(name="Charlie", email="charlie@example.com") # Will raise ValidationError
    pass
except ValidationError as e:
    print(f"\nValidation Error for user3 (missing id):\n{e}")

# Example 4: Invalid data (invalid email format)
try:
    # user4 = User(id=4, email="invalid-email") # Will raise ValidationError
    pass
except ValidationError as e:
    print(f"\nValidation Error for user4 (invalid email):\n{e}")

# 2. Nested Models and Lists

class Item(BaseModel):
    name: str
    price: float
    tags: List[str] = []

class Order(BaseModel):
    order_id: str
    customer_id: int
    items: List[Item]
    status: Literal["pending", "completed", "cancelled"] = "pending"

# Example 5: Creating a nested model
try:
    order1 = Order(
        order_id="ORD001",
        customer_id=101,
        items=[
            Item(name="Laptop", price=1200.00, tags=["electronics", "computer"]),
            Item(name="Mouse", price=25.50)
        ],
        status="completed"
    )
    print(f"\nOrder 1: {order1.model_dump_json(indent=2)}")
except ValidationError as e:
    print(f"Validation Error: {e}")

# 3. Using Field for more validation and metadata

class Product(BaseModel):
    product_id: str = Field(..., min_length=5, max_length=10, description="Unique product identifier")
    name: str = Field(..., example="Wireless Headphones")
    price: float = Field(..., gt=0, description="Price must be greater than zero")
    quantity: int = Field(1, ge=1, le=100, description="Quantity in stock")

# Example 6: Valid product
try:
    product1 = Product(product_id="PROD123", name="Keyboard", price=75.99, quantity=10)
    print(f"\nProduct 1: {product1.model_dump_json(indent=2)}")
except ValidationError as e:
    print(f"Validation Error: {e}")

# Example 7: Invalid product (price <= 0)
try:
    # product2 = Product(product_id="PROD456", name="Monitor", price=0, quantity=5) # Will raise ValidationError
    pass
except ValidationError as e:
    print(f"\nValidation Error for product2 (price <= 0):\n{e}")

# 4. Integrating with FastAPI (conceptual example)
#    - FastAPI leverages Pydantic models for request body validation, response serialization,
#      and automatic OpenAPI (Swagger) documentation generation.

# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None

# @app.post("/items/")
# async def create_item(item: Item):
#     return item

# When you send a POST request to /items/ with JSON data, FastAPI (using Pydantic)
# will automatically validate the incoming data against the Item model.
# If validation fails, it returns a detailed error response.
