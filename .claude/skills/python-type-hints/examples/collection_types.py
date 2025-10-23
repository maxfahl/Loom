# examples/collection_types.py

# This file demonstrates type hints for common Python collection types.
# Using native generics (PEP 585) for Python 3.9+.

# 1. List: list[Type]
def process_names(names: list[str]) -> list[str]:
    return [name.upper() for name in names]

def sum_numbers(numbers: list[int]) -> int:
    return sum(numbers)

print(f"Processed names: {process_names(['alice', 'bob'])}")
print(f"Sum of numbers: {sum_numbers([1, 2, 3, 4])}")

# 2. Dictionary: dict[KeyType, ValueType]
def get_user_age(users: dict[str, int], name: str) -> int | None:
    return users.get(name)

def update_scores(scores: dict[str, float], new_score: float) -> dict[str, float]:
    scores["latest"] = new_score
    return scores

user_ages = {"Alice": 30, "Bob": 24}
print(f"Alice's age: {get_user_age(user_ages, 'Alice')}")
print(f"Charlie's age: {get_user_age(user_ages, 'Charlie')}")

current_scores = {"math": 90.5, "science": 88.0}
print(f"Updated scores: {update_scores(current_scores, 95.0)}")

# 3. Set: set[Type]
def get_unique_elements(elements: list[str]) -> set[str]:
    return set(elements)

def check_membership(s: set[int], value: int) -> bool:
    return value in s

print(f"Unique elements: {get_unique_elements(['apple', 'banana', 'apple'])}")
print(f"Is 3 in {{1, 2, 3}}: {check_membership({1, 2, 3}, 3)}")

# 4. Tuple: tuple[Type1, Type2, ...] (fixed size, heterogeneous)
#           tuple[Type, ...] (variable size, homogeneous)

def get_coordinates() -> tuple[float, float]:
    return (10.5, 20.3)

def process_user_info(info: tuple[int, str, bool]) -> str:
    user_id, name, is_active = info
    return f"User ID: {user_id}, Name: {name}, Active: {is_active}"

def log_events(events: tuple[str, ...]) -> None:
    for event in events:
        print(f"Event: {event}")

print(f"Coordinates: {get_coordinates()}")
print(f"User info: {process_user_info((1, 'Alice', True))}")
log_events(("login", "logout", "purchase"))

# 5. Deque (from collections module)
from collections import deque

def process_queue(q: deque[str]) -> None:
    while q:
        print(f"Processing: {q.popleft()}")

my_queue: deque[str] = deque(["task1", "task2", "task3"])
process_queue(my_queue)

# 6. FrozenSet (immutable set)
from typing import FrozenSet

def get_immutable_tags(tags: FrozenSet[str]) -> FrozenSet[str]:
    # tags.add("new") # This would be a type error
    return tags

immutable_tags: FrozenSet[str] = frozenset(["python", "typing"])
print(f"Immutable tags: {get_immutable_tags(immutable_tags)}")

# 7. ChainMap (from collections module)
from collections import ChainMap

def get_config_value(config: ChainMap[str, Any], key: str) -> Any:
    return config.get(key)

default_config = {"debug": False, "port": 8080}
user_config = {"port": 9000}

combined_config: ChainMap[str, Any] = ChainMap(user_config, default_config)
print(f"Debug setting: {get_config_value(combined_config, 'debug')}")
print(f"Port setting: {get_config_value(combined_config, 'port')}")
