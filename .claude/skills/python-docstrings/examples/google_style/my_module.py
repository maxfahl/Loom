def greet(name: str) -> str:
    """Greets a person by their name.

    This function takes a string `name` as input and returns a greeting message.

    Args:
        name (str): The name of the person to greet.

    Returns:
        str: A personalized greeting message.

    Examples:
        >>> greet("Alice")
        'Hello, Alice!'
        >>> greet("Bob")
        'Hello, Bob!'
    """
    return f"Hello, {name}!"

def add_numbers(a: int, b: int) -> int:
    """Adds two integers and returns their sum.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The sum of the two integers.

    Raises:
        TypeError: If `a` or `b` are not integers.
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Both inputs must be integers.")
    return a + b
