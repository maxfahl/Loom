# patterns/runtime_type_checking.py

# This file demonstrates various approaches to runtime type checking in Python.
# While type hints are primarily for static analysis, sometimes you need to
# verify types at runtime, especially for external inputs or dynamic scenarios.

from typing import Union, List, Dict, Any, get_origin, get_args

# 1. Basic `isinstance()` checks
#    - Most common and straightforward for built-in types.

def process_value(value: Union[str, int]) -> str:
    if isinstance(value, str):
        return f"String value: {value.upper()}"
    elif isinstance(value, int):
        return f"Integer value: {value * 2}"
    else:
        # This branch should ideally not be reached with proper static typing
        # but serves as a runtime fallback.
        raise TypeError(f"Unsupported type: {type(value)}")

print(f"Process 'hello': {process_value('hello')}")
print(f"Process 10: {process_value(10)}")
# print(f"Process 10.5: {process_value(10.5)}") # Will raise TypeError at runtime

# 2. Runtime checks for collections (more complex)
#    - `isinstance` alone doesn't check generic types (e.g., `list[str]` vs `list[int]`)

def process_list_of_strings(data: List[str]) -> List[str]:
    if not isinstance(data, list):
        raise TypeError("Expected a list")
    for item in data:
        if not isinstance(item, str):
            raise TypeError("Expected list of strings")
    return [s.strip() for s in data]

try:
    print(f"Process list of strings: {process_list_of_strings([' a ', ' b '])}")
    # process_list_of_strings(['a', 1]) # Will raise TypeError at runtime
except TypeError as e:
    print(f"Error: {e}")

# 3. Using `get_origin` and `get_args` from `typing` for more advanced checks
#    - Useful for inspecting generic types at runtime.

def check_type_runtime(value: Any, expected_type: Any) -> bool:
    origin = get_origin(expected_type)
    args = get_args(expected_type)

    if origin is None: # Not a generic type (e.g., str, int)
        return isinstance(value, expected_type)
    elif origin is list:
        if not isinstance(value, list):
            return False
        if not args: # Untyped list
            return True
        item_type = args[0]
        return all(check_type_runtime(item, item_type) for item in value)
    elif origin is dict:
        if not isinstance(value, dict):
            return False
        if not args: # Untyped dict
            return True
        key_type, value_type = args
        return all(check_type_runtime(k, key_type) and check_type_runtime(v, value_type) for k, v in value.items())
    elif origin is Union:
        return any(check_type_runtime(value, arg) for arg in args)
    # Add more origins as needed (e.g., tuple, set, Optional)
    return False

print(f"\nRuntime type check for list[str]:")
print(f"  ['a', 'b'] is list[str]: {check_type_runtime(['a', 'b'], List[str])}")
print(f"  ['a', 1] is list[str]: {check_type_runtime(['a', 1], List[str])}")
print(f"  {{'a': 1}} is dict[str, int]: {check_type_runtime({'a': 1}, Dict[str, int])}")
print(f"  {{'a': 'b'}} is dict[str, int]: {check_type_runtime({'a': 'b'}, Dict[str, int])}")
print(f"  10 is Union[str, int]: {check_type_runtime(10, Union[str, int])}")

# 4. Using `pydantic` for robust runtime validation (recommended for complex data)
#    - See `data_validation.py` for more comprehensive examples.

from pydantic import BaseModel

class Config(BaseModel):
    host: str
    port: int
    debug: bool = False

def load_config(raw_data: Dict[str, Any]) -> Config:
    try:
        return Config(**raw_data)
    except ValidationError as e:
        raise ValueError(f"Invalid configuration data: {e}") from e

valid_config_data = {"host": "localhost", "port": 8080}
invalid_config_data = {"host": "localhost", "port": "eighty"}

try:
    config = load_config(valid_config_data)
    print(f"\nLoaded config: {config.model_dump_json(indent=2)}")
except ValueError as e:
    print(f"Error loading config: {e}")

try:
    config = load_config(invalid_config_data)
    print(f"Loaded config: {config.model_dump_json(indent=2)}")
except ValueError as e:
    print(f"Error loading config: {e}")

# 5. Using `beartype` for O(1) runtime type checking (third-party library)
#    - `beartype` is a decorator that adds runtime type checking with minimal overhead.
#    - Requires `pip install beartype`

# from beartype import beartype

# @beartype
# def divide(numerator: int, denominator: int) -> float:
#     return numerator / denominator

# try:
#     print(f"\nDivide 10 by 2: {divide(10, 2)}")
#     # print(f"Divide 10 by 'a': {divide(10, 'a')}") # Will raise BeartypeCallHintParamViolation at runtime
# except Exception as e:
#     print(f"Error with beartype: {e}")
