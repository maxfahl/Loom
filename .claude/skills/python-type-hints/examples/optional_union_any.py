# examples/optional_union_any.py

# This file demonstrates the usage of Optional, Union, and Any in Python type hints.

from typing import Union, Optional, Any

# 1. Union: Union[Type1, Type2, ...]
#    - Indicates that a variable can be one of several types.
#    - In Python 3.10+, you can use the `|` operator for Union.

def process_id(id: Union[str, int]) -> str:
    if isinstance(id, int):
        return f"ID (int): {id}"
    return f"ID (str): {id.upper()}"

print(f"Processed ID: {process_id(123)}")
print(f"Processed ID: {process_id('abc-123')}")

# Using `|` operator (Python 3.10+)
def process_value(value: str | float) -> str:
    if isinstance(value, float):
        return f"Value (float): {value:.2f}"
    return f"Value (str): {value.strip()}"

print(f"Processed value: {process_value(123.456)}")
print(f"Processed value: {process_value('  hello  ')}")

# 2. Optional: Optional[Type]
#    - Syntactic sugar for Union[Type, None].
#    - Indicates that a variable can be of a certain type or None.

def get_username(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Alice"
    return None

user_name = get_username(1)
if user_name is not None:
    print(f"Username: {user_name}")
else:
    print("User not found.")

user_name_none = get_username(2)
if user_name_none is not None:
    print(f"Username: {user_name_none}")
else:
    print("User not found.")

# 3. Any: Any
#    - Indicates that a variable can be of any type.
#    - Bypasses type checking for that variable. Use sparingly.

def handle_flexible_data(data: Any) -> Any:
    print(f"Received data of type: {type(data).__name__}")
    if isinstance(data, (int, float)):
        return data * 2
    elif isinstance(data, str):
        return data.upper()
    return data

print(f"Flexible data (int): {handle_flexible_data(10)}")
print(f"Flexible data (str): {handle_flexible_data('test')}")
print(f"Flexible data (list): {handle_flexible_data([1, 2, 3])}")

# Anti-pattern: Overusing Any
# While `Any` can be useful for quick prototyping or when dealing with highly dynamic data,
# overusing it defeats the purpose of type hints and reduces type safety.

# BAD:
def process_anything(item: Any) -> Any:
    # No type safety here, mypy won't catch errors like item.non_existent_method()
    return item

# GOOD: Prefer specific types, Union, or runtime checks with `unknown` (conceptually) or `object`
# If you truly don't know the type, use runtime checks to narrow it down.
def process_unknown_item(item: object) -> str:
    if isinstance(item, str):
        return f"String: {item.strip()}"
    elif isinstance(item, int):
        return f"Integer: {item * 10}"
    return f"Unknown type: {type(item).__name__}"

print(f"Processed unknown item (str): {process_unknown_item('  data  ')}")
print(f"Processed unknown item (int): {process_unknown_item(5)}")
print(f"Processed unknown item (bool): {process_unknown_item(True)}")
