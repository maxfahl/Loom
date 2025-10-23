# examples/callable_typeddict.py

# This file demonstrates the usage of Callable and TypedDict in Python type hints.

from typing import Callable, TypedDict, List

# 1. Callable: Callable[[Arg1Type, Arg2Type, ...], ReturnType]
#    - Used to type hint functions, specifying their argument types and return type.

# Example 1: Simple callback
def execute_callback(callback: Callable[[str], None], message: str) -> None:
    print("Executing callback...")
    callback(message)

def my_printer(text: str) -> None:
    print(f"Printer received: {text}")

execute_callback(my_printer, "Hello from Callable!")

# Example 2: Function that returns a value
def apply_operation(op: Callable[[int, int], int], a: int, b: int) -> int:
    return op(a, b)

def multiply(x: int, y: int) -> int:
    return x * y

def add(x: int, y: int) -> int:
    return x + y

print(f"Result of multiply: {apply_operation(multiply, 5, 3)}")
print(f"Result of add: {apply_operation(add, 10, 7)}")

# Example 3: Callable with no arguments or no return
def run_task(task: Callable[[], None]) -> None:
    print("Running task...")
    task()

def simple_task() -> None:
    print("Simple task completed.")

run_task(simple_task)

# 2. TypedDict: TypedDict
#    - Used to define dictionaries with a fixed set of keys and specific value types.
#    - Provides type checking for dictionary access, similar to interfaces in other languages.

class UserProfile(TypedDict):
    name: str
    age: int
    email: str
    is_active: bool
    tags: List[str] # Using native generic list

# Example 1: Creating a TypedDict instance
user1: UserProfile = {
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com",
    "is_active": True,
    "tags": ["developer", "python"]
}

print(f"User 1: {user1}")
print(f"User 1 name: {user1['name']}")

# Example 2: Type checking for missing or incorrect keys/types
# user2: UserProfile = {
#     "name": "Bob",
#     "age": "twenty", # Mypy error: Incompatible types in assignment
#     "email": "bob@example.com",
#     "is_active": False
#     # Mypy error: Missing key 'tags'
# }

# Example 3: Function accepting a TypedDict
def display_user_profile(profile: UserProfile) -> None:
    print(f"\n--- User Profile ---")
    print(f"Name: {profile['name']}")
    print(f"Age: {profile['age']}")
    print(f"Email: {profile['email']}")
    print(f"Active: {profile['is_active']}")
    print(f"Tags: {profile['tags']}")

display_user_profile(user1)

# Example 4: Optional keys in TypedDict
class Product(TypedDict, total=False): # total=False makes all keys optional by default
    name: str
    price: float
    description: str
    in_stock: bool

product1: Product = {
    "name": "Laptop",
    "price": 1200.00,
    "in_stock": True
}

product2: Product = {
    "name": "Mouse",
    "price": 25.00,
    "description": "Wireless ergonomic mouse"
}

print(f"\nProduct 1: {product1}")
print(f"Product 2: {product2}")

# You can also make specific keys optional while others are required
class Book(TypedDict):
    title: str
    author: str
    isbn: str
    pages: int
    publisher: NotRequired[str] # Requires `from typing import NotRequired` (Python 3.11+)

# For Python < 3.11, use `total=False` and then mark required fields explicitly
# class Book(TypedDict, total=False):
#     title: Required[str]
#     author: Required[str]
#     isbn: Required[str]
#     pages: Required[int]
#     publisher: str

# Note: NotRequired and Required are available from Python 3.11
# For older versions, managing optional/required keys in TypedDict can be more verbose.
