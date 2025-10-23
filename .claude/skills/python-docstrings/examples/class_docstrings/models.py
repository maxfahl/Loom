class User:
    """Represents a user in the system.

    This class stores user information such as ID, name, and email.

    Attributes:
        user_id (int): The unique identifier for the user.
        name (str): The full name of the user.
        email (str): The email address of the user.
    """
    def __init__(self, user_id: int, name: str, email: str):
        """Initializes a new User instance.

        Args:
            user_id (int): The unique identifier for the user.
            name (str): The full name of the user.
            email (str): The email address of the user.
        """
        self.user_id = user_id
        self.name = name
        self.email = email

    def get_info(self) -> str:
        """Returns a formatted string with user information.

        Returns:
            str: A string containing the user's ID, name, and email.
        """
        return f"User ID: {self.user_id}, Name: {self.name}, Email: {self.email}"


class Product:
    """Represents a product available for sale.

    This class holds details about a product, including its ID, name, and price.

    Attributes:
        product_id (str): The unique identifier for the product.
        name (str): The name of the product.
        price (float): The price of the product.
    """
    def __init__(self, product_id: str, name: str, price: float):
        """Initializes a new Product instance.

        Args:
            product_id (str): The unique identifier for the product.
            name (str): The name of the product.
            price (float): The price of the product.
        """
        self.product_id = product_id
        self.name = name
        self.price = price

    def display_price(self) -> str:
        """Returns the product price formatted as a currency string.

        Returns:
            str: The price formatted with two decimal places.
        """
        return f"${self.price:.2f}"
