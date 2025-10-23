import argparse
import csv
import json
import os
from faker import Faker

def generate_users(num_users):
    fake = Faker()
    users = []
    for i in range(num_users):
        first_name = fake.first_name()
        last_name = fake.last_name()
        users.append({
            "id": i + 1,
            "username": f"{first_name.lower()}.{last_name.lower()}{i}",
            "email": fake.email(),
            "password": fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True),
            "first_name": first_name,
            "last_name": last_name,
            "address": fake.address().replace('\n', ', '),
            "phone_number": fake.phone_number()
        })
    return users

def generate_products(num_products):
    fake = Faker()
    products = []
    for i in range(num_products):
        products.append({
            "id": fake.uuid4(),
            "name": fake.word().capitalize() + " " + fake.color_name() + " " + fake.product_name(),
            "description": fake.paragraph(nb_sentences=3),
            "price": round(fake.random_number(digits=2) + fake.random_sample_element(elements=[0.99, 0.49, 0.00]), 2),
            "category": fake.random_element(elements=('Electronics', 'Books', 'Clothing', 'Home & Kitchen', 'Sports')),
            "in_stock": fake.boolean(chance_of_getting_true=90)
        })
    return products

def main():
    parser = argparse.ArgumentParser(
        description="Generate realistic test data for k6 load testing."
    )
    parser.add_argument(
        "-t", "--type",
        choices=["users", "products"],
        required=True,
        help="Type of data to generate (users or products)."
    )
    parser.add_argument(
        "-n", "--number",
        type=int,
        default=100,
        help="Number of data entries to generate. Default is 100."
    )
    parser.add_argument(
        "-f", "--format",
        choices=["json", "csv"],
        default="json",
        help="Output format (json or csv). Default is json."
    )
    parser.add_argument(
        "-o", "--output",
        default="data",
        help="Output directory for the generated file. Default is 'data'."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print data to console instead of saving to file."
    )

    args = parser.parse_args()

    if args.type == "users":
        data = generate_users(args.number)
        filename = f"users.{args.format}"
    elif args.type == "products":
        data = generate_products(args.number)
        filename = f"products.{args.format}"
    else:
        print("Error: Invalid data type specified.")
        return

    if args.dry_run:
        if args.format == "json":
            print(json.dumps(data, indent=2))
        else:
            # For CSV dry run, print headers and first few rows
            if data:
                writer = csv.writer(os.sys.stdout)
                writer.writerow(data[0].keys())
                for row in data[:5]: # Print first 5 rows for dry run
                    writer.writerow(row.values())
            else:
                print("No data to display.")
        return

    os.makedirs(args.output, exist_ok=True)
    filepath = os.path.join(args.output, filename)

    if args.format == "json":
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    elif args.format == "csv":
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if data:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
    
    print(f"Successfully generated {args.number} {args.type} and saved to {filepath}")

if __name__ == "__main__":
    try:
        # Ensure faker is installed: pip install Faker
        main()
    except ImportError:
        print("Error: 'Faker' library not found. Please install it using: pip install Faker")
    except Exception as e:
        print(f"An error occurred: {e}")
