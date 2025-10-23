from typing import Iterator

def fibonacci_sequence(n: int) -> Iterator[int]:
    """Generates the Fibonacci sequence up to n terms.

    The Fibonacci sequence is a series of numbers where each number is the sum
    of the two preceding ones, usually starting with 0 and 1.

    Args:
        n (int): The number of terms to generate in the sequence.

    Yields:
        int: The next number in the Fibonacci sequence.

    Raises:
        ValueError: If `n` is a negative integer.

    Examples:
        >>> list(fibonacci_sequence(5))
        [0, 1, 1, 2, 3]
        >>> list(fibonacci_sequence(0))
        []
    """
    if n < 0:
        raise ValueError("Number of terms cannot be negative.")
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

def even_numbers(start: int, end: int) -> Iterator[int]:
    """Generates even numbers within a specified range.

    Args:
        start (int): The starting number of the range (inclusive).
        end (int): The ending number of the range (inclusive).

    Yields:
        int: The next even number in the range.

    Examples:
        >>> list(even_numbers(1, 10))
        [2, 4, 6, 8, 10]
        >>> list(even_numbers(0, 0))
        [0]
    """
    for i in range(start, end + 1):
        if i % 2 == 0:
            yield i
