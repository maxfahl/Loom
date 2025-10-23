# examples/generics_protocols.py

# This file demonstrates the usage of TypeVar for generics and Protocol for structural subtyping.

from typing import TypeVar, Generic, Protocol, runtime_checkable

# 1. TypeVar: For defining generic types
#    - Allows you to write functions or classes that can operate on different types
#      while maintaining type safety.

T = TypeVar('T') # Declare a type variable

class Box(Generic[T]):
    def __init__(self, content: T):
        self.content = content

    def get_content(self) -> T:
        return self.content

    def set_content(self, new_content: T) -> None:
        self.content = new_content

def first_element(items: list[T]) -> T:
    return items[0]

int_box = Box(10)
str_box = Box("hello")

print(f"Int box content: {int_box.get_content()}")
print(f"Str box content: {str_box.get_content()}")

int_box.set_content(20)
# str_box.set_content(123) # Mypy error: Argument 1 to "set_content" of "Box" has incompatible type "int"; expected "str"

print(f"First element of [1, 2, 3]: {first_element([1, 2, 3])}")
print(f"First element of ['a', 'b', 'c']: {first_element(['a', 'b', 'c'])}")

# TypeVar with bounds or constraints
# Bounded TypeVar: T = TypeVar('T', bound=Animal)
# Constrained TypeVar: T = TypeVar('T', str, bytes)

# 2. Protocol: For structural subtyping (duck typing)
#    - Defines an interface that classes can implicitly implement by having the required methods/attributes.
#    - No need for explicit inheritance.

@runtime_checkable # Allows isinstance() checks at runtime
class SupportsLen(Protocol):
    def __len__(self) -> int:
        ...

def get_length(obj: SupportsLen) -> int:
    return len(obj)

class MyList:
    def __init__(self, items):
        self.items = items
    def __len__(self) -> int:
        return len(self.items)

class MyString:
    def __init__(self, text: str):
        self.text = text
    def __len__(self) -> int:
        return len(self.text)

# Classes implicitly implement SupportsLen because they have a __len__ method
print(f"Length of [1, 2, 3]: {get_length([1, 2, 3])}")
print(f"Length of 'hello': {get_length('hello')}")
print(f"Length of MyList: {get_length(MyList([10, 20]))}")
print(f"Length of MyString: {get_length(MyString("protocol"))}")

# Using isinstance with runtime_checkable
my_obj = MyList([1, 2, 3])
if isinstance(my_obj, SupportsLen):
    print(f"MyList instance supports len: {get_length(my_obj)}")

# Protocol for a more complex interface
class Greeter(Protocol):
    name: str
    def greet(self) -> str:
        ...

class EnglishGreeter:
    def __init__(self, name: str):
        self.name = name
    def greet(self) -> str:
        return f"Hello, {self.name}!"

class SpanishGreeter:
    def __init__(self, name: str):
        self.name = name
    def greet(self) -> str:
        return f"¡Hola, {self.name}!"

def say_hello(greeter: Greeter) -> None:
    print(greeter.greet())

say_hello(EnglishGreeter("Alice"))
say_hello(SpanishGreeter("Bob"))

# Mypy will check if the object passed to say_hello conforms to the Greeter protocol.
# class BadGreeter:
#     def __init__(self, name: str):
#         self.name = name
#     # Missing greet method

# say_hello(BadGreeter("Charlie")) # Mypy error: Argument 1 to "say_hello" has incompatible type "BadGreeter"; expected "Greeter"
