# examples/basic_types.py

# This file demonstrates basic type hints for common Python types.

# 1. Numeric Types: int, float
def add_numbers(a: int, b: int) -> int:
    return a + b

def calculate_average(numbers: list[float]) -> float:
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)

print(f"Add numbers (int): {add_numbers(5, 3)}")
print(f"Calculate average (float): {calculate_average([10.5, 20.0, 30.5])}")

# 2. String Type: str
def greet(name: str) -> str:
    return f"Hello, {name.capitalize()}!"

def concatenate_strings(s1: str, s2: str) -> str:
    return s1 + s2

print(f"Greet: {greet('alice')}")
print(f"Concatenate: {concatenate_strings('Hello', ' World')}")

# 3. Boolean Type: bool
def is_even(number: int) -> bool:
    return number % 2 == 0

def check_status(is_active: bool, has_permission: bool) -> bool:
    return is_active and has_permission

print(f"Is 4 even: {is_even(4)}")
print(f"Check status (True, False): {check_status(True, False)}")

# 4. Bytes Type: bytes
def encode_string(text: str, encoding: str = 'utf-8') -> bytes:
    return text.encode(encoding)

def decode_bytes(data: bytes, encoding: str = 'utf-8') -> str:
    return data.decode(encoding)

encoded = encode_string("Python Type Hints")
print(f"Encoded string: {encoded}")
print(f"Decoded bytes: {decode_bytes(encoded)}")

# 5. None Type: None
#    - Used to indicate that a function does not return a value.
#    - For variables that can be None, use Optional or Union (see optional_union_any.py).
def log_message(message: str) -> None:
    print(f"LOG: {message}")

log_message("This is a log entry.")

# 6. Object Type: object
#    - The base type for all classes. Use sparingly, as it provides little type safety.
#    - Prefer more specific types or Any if you truly don't know the type.
def process_any_object(obj: object) -> str:
    return f"Processed object of type {type(obj).__name__}"

print(process_any_object(123))
print(process_any_object("hello"))
print(process_any_object([1, 2, 3]))

# 7. Ellipsis Type: ...
#    - Used in conjunction with Tuple to indicate an arbitrary number of items.
#    - See collection_types.py for more details.

def print_args(*args: str) -> None:
    print("Arguments:", args)

print_args("a", "b", "c")
