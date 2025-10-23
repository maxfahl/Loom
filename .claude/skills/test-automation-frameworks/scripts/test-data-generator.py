import argparse
import json
import random
import string
from datetime import datetime, timedelta

# test-data-generator.py
#
# Description:
#   This script generates various types of realistic, randomized test data.
#   It can be used to create data for users, products, orders, or custom data structures.
#   The output can be printed to console or saved to a JSON file.
#
# Usage:
#   python test-data-generator.py <data_type> [options]
#
# Arguments:
#   <data_type> : The type of data to generate (e.g., user, product, order, custom).
#                 Use 'custom' with --schema to define your own data structure.
#
# Options:
#   -n, --count       : Number of data records to generate (default: 1).
#   -o, --output      : Output file path (e.g., 'data.json'). If not provided, prints to stdout.
#   -s, --schema      : JSON string or file path for custom data schema. Required for 'custom' data_type.
#                       Example: '{"name": "string", "age": "int:18-60", "email": "email"}'
#   -p, --pretty      : Pretty print JSON output.
#   -h, --help        : Show this help message and exit.
#
# Examples:
#   python test-data-generator.py user --count 5 --output users.json --pretty
#   python test-data-generator.py product -n 3
#   python test-data-generator.py custom -s '{"id": "uuid", "status": "choice:active,inactive", "timestamp": "datetime"}' -o custom_data.json
#   python test-data-generator.py custom -s schema.json
#
# Data Types and Supported Field Types:
#   - string          : Random string of alphanumeric characters.
#   - int:<min>-<max> : Random integer within a range (e.g., 'int:1-100').
#   - float:<min>-<max> : Random float within a range (e.g., 'float:0.0-99.9').
#   - boolean         : Random boolean (true/false).
#   - email           : Random email address.
#   - uuid            : UUID v4 string.
#   - datetime        : ISO formatted datetime string.
#   - date            : ISO formatted date string.
#   - choice:<opt1,opt2,...> : Random choice from a comma-separated list (e.g., 'choice:pending,approved,rejected').
#   - firstname       : Random first name.
#   - lastname        : Random last name.
#   - fullname        : Random full name.
#   - address         : Random street address.
#   - city            : Random city name.
#   - country         : Random country name.
#   - zipcode         : Random 5-digit zipcode.
#   - phone           : Random phone number.
#   - url             : Random URL.
#   - lorem           : Lorem ipsum text.
#
# Note: For custom schemas, field types are specified as strings. For example, "age": "int:18-60".

class TestDataGenerator:
    def __init__(self):
        self.first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Heidi"]
        self.last_names = ["Smith", "Jones", "Williams", "Brown", "Davis", "Miller", "Wilson", "Moore"]
        self.cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio"]
        self.countries = ["USA", "Canada", "Mexico", "UK", "Germany", "France", "Japan", "Australia"]
        self.product_adjectives = ["Awesome", "Super", "Fantastic", "Great", "Amazing", "Best"]
        self.product_nouns = ["Widget", "Gadget", "Doodad", "Thingamajig", "Gizmo", "Product"]

    def _generate_string(self, length=10):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def _generate_int(self, min_val, max_val):
        return random.randint(min_val, max_val)

    def _generate_float(self, min_val, max_val):
        return round(random.uniform(min_val, max_val), 2)

    def _generate_boolean(self):
        return random.choice([True, False])

    def _generate_email(self):
        return f"{self._generate_string(5).lower()}@{self._generate_string(5).lower()}.com"

    def _generate_uuid(self):
        # Simplified UUID generation for example purposes
        return f"{ ''.join(random.choices(string.hexdigits, k=8))}-{''.join(random.choices(string.hexdigits, k=4))}-4{''.join(random.choices(string.hexdigits, k=3))}-{''.join(random.choices(string.hexdigits, k=4))}-{''.join(random.choices(string.hexdigits, k=12))}"

    def _generate_datetime(self):
        now = datetime.now()
        random_days = random.randint(0, 365)
        random_seconds = random.randint(0, 86400)
        dt = now - timedelta(days=random_days, seconds=random_seconds)
        return dt.isoformat()

    def _generate_date(self):
        return self._generate_datetime().split('T')[0]

    def _generate_choice(self, options):
        return random.choice(options)

    def _generate_firstname(self):
        return random.choice(self.first_names)

    def _generate_lastname(self):
        return random.choice(self.last_names)

    def _generate_fullname(self):
        return f"{self._generate_firstname()} {self._generate_lastname()}"

    def _generate_address(self):
        return f"{random.randint(1, 999)} {self._generate_string(7).capitalize()} St."

    def _generate_city(self):
        return random.choice(self.cities)

    def _generate_country(self):
        return random.choice(self.countries)

    def _generate_zipcode(self):
        return ''.join(random.choices(string.digits, k=5))

    def _generate_phone(self):
        return f"({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"

    def _generate_url(self):
        return f"https://www.{self._generate_string(5).lower()}.com/{self._generate_string(3).lower()}"

    def _generate_lorem(self, words=10):
        lorem_ipsum_words = "Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua Ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum".split()
        return ' '.join(random.sample(lorem_ipsum_words, words))

    def generate_field(self, field_type):
        if field_type == "string":
            return self._generate_string()
        elif field_type.startswith("int:"):
            _, r = field_type.split(':', 1)
            min_val, max_val = map(int, r.split('-'))
            return self._generate_int(min_val, max_val)
        elif field_type.startswith("float:"):
            _, r = field_type.split(':', 1)
            min_val, max_val = map(float, r.split('-'))
            return self._generate_float(min_val, max_val)
        elif field_type == "boolean":
            return self._generate_boolean()
        elif field_type == "email":
            return self._generate_email()
        elif field_type == "uuid":
            return self._generate_uuid()
        elif field_type == "datetime":
            return self._generate_datetime()
        elif field_type == "date":
            return self._generate_date()
        elif field_type.startswith("choice:"):
            _, options_str = field_type.split(':', 1)
            options = options_str.split(',')
            return self._generate_choice(options)
        elif field_type == "firstname":
            return self._generate_firstname()
        elif field_type == "lastname":
            return self._generate_lastname()
        elif field_type == "fullname":
            return self._generate_fullname()
        elif field_type == "address":
            return self._generate_address()
        elif field_type == "city":
            return self._generate_city()
        elif field_type == "country":
            return self._generate_country()
        elif field_type == "zipcode":
            return self._generate_zipcode()
        elif field_type == "phone":
            return self._generate_phone()
        elif field_type == "url":
            return self._generate_url()
        elif field_type == "lorem":
            return self._generate_lorem()
        else:
            raise ValueError(f"Unknown field type: {field_type}")

    def generate_user_data(self):
        return {
            "id": self._generate_uuid(),
            "firstName": self._generate_firstname(),
            "lastName": self._generate_lastname(),
            "email": self._generate_email(),
            "age": self._generate_int(18, 99),
            "isActive": self._generate_boolean(),
            "registeredDate": self._generate_date(),
            "address": {
                "street": self._generate_address(),
                "city": self._generate_city(),
                "zipCode": self._generate_zipcode(),
                "country": self._generate_country()
            }
        }

    def generate_product_data(self):
        return {
            "id": self._generate_uuid(),
            "name": f"{random.choice(self.product_adjectives)} {random.choice(self.product_nouns)} {self._generate_string(3).upper()}",
            "description": self._generate_lorem(words=20),
            "price": self._generate_float(5.0, 1000.0),
            "inStock": self._generate_boolean(),
            "category": self._generate_choice(["Electronics", "Books", "Home", "Clothing", "Sports"]),
            "sku": self._generate_string(12).upper()
        }

    def generate_order_data(self):
        return {
            "orderId": self._generate_uuid(),
            "userId": self._generate_uuid(), # Assuming a user exists
            "orderDate": self._generate_datetime(),
            "totalAmount": self._generate_float(10.0, 5000.0),
            "status": self._generate_choice(["pending", "processing", "shipped", "delivered", "cancelled"]),
            "items": [
                {
                    "productId": self._generate_uuid(),
                    "quantity": self._generate_int(1, 5),
                    "price": self._generate_float(5.0, 500.0)
                } for _ in range(random.randint(1, 3)) # 1 to 3 items per order
            ]
        }

    def generate_custom_data(self, schema):
        data = {}
        for key, field_type in schema.items():
            data[key] = self.generate_field(field_type)
        return data

def main():
    parser = argparse.ArgumentParser(
        description="Generate various types of realistic, randomized test data.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("data_type", type=str, help="Type of data to generate (user, product, order, custom).")
    parser.add_argument("-n", "--count", type=int, default=1, help="Number of data records to generate (default: 1).")
    parser.add_argument("-o", "--output", type=str, help="Output file path (e.g., 'data.json'). If not provided, prints to stdout.")
    parser.add_argument("-s", "--schema", type=str, help=
        "JSON string or file path for custom data schema. Required for 'custom' data_type.\n"
        "Example: '{\"name\": \"string\", \"age\": \"int:18-60\", \"email\": \"email\"}'\n"
        "Supported field types: string, int:<min>-<max>, float:<min>-<max>, boolean, email, uuid, datetime, date, choice:<opt1,opt2,...>, firstname, lastname, fullname, address, city, country, zipcode, phone, url, lorem."
    )
    parser.add_argument("-p", "--pretty", action="store_true", help="Pretty print JSON output.")

    args = parser.parse_args()

    generator = TestDataGenerator()
    generated_data = []

    if args.data_type == "user":
        for _ in range(args.count):
            generated_data.append(generator.generate_user_data())
    elif args.data_type == "product":
        for _ in range(args.count):
            generated_data.append(generator.generate_product_data())
    elif args.data_type == "order":
        for _ in range(args.count):
            generated_data.append(generator.generate_order_data())
    elif args.data_type == "custom":
        if not args.schema:
            parser.error("'--schema' is required for 'custom' data_type.")
        
        custom_schema = None
        try:
            # Try to load as JSON string
            custom_schema = json.loads(args.schema)
        except json.JSONDecodeError:
            # If not a JSON string, try to load as a file path
            try:
                with open(args.schema, 'r') as f:
                    custom_schema = json.load(f)
            except FileNotFoundError:
                parser.error(f"Schema file not found: {args.schema}")
            except json.JSONDecodeError:
                parser.error(f"Invalid JSON in schema file: {args.schema}")

        if not custom_schema:
            parser.error("Could not parse custom schema. Ensure it's valid JSON string or file.")

        for _ in range(args.count):
            generated_data.append(generator.generate_custom_data(custom_schema))
    else:
        parser.error(f"Unknown data type: {args.data_type}. Choose from user, product, order, or custom.")

    output_content = json.dumps(generated_data, indent=4 if args.pretty else None)

    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write(output_content)
            print(f"Successfully generated {args.count} records to {args.output}")
        except IOError as e:
            print(f"Error writing to file {args.output}: {e}")
            exit(1)
    else:
        print(output_content)

if __name__ == "__main__":
    main()
