
#!/usr/bin/env python3
"""
generate-synthetic-data.py: A script to generate synthetic data based on a JSON schema.

This script reads a JSON schema defining the structure and data types for synthetic data
generation. It uses the 'faker' library to produce realistic-looking data,
which is useful for development and testing in non-production environments.

Usage:
    python3 generate-synthetic-data.py -s <schema_file.json> -o <output_file.json> -c <count> [--dry-run] [--verbose]

Examples:
    # Generate 10 records based on 'user_schema.json' and save to 'synthetic_users.json'
    python3 generate-synthetic-data.py -s user_schema.json -o synthetic_users.json -c 10

    # Dry run: show generated data without saving
    python3 generate-synthetic-data.py -s user_schema.json -c 5 --dry-run

Configuration:
    The schema file should be a JSON file with a structure like this:
    {
        "record_type": "user",
        "fields": {
            "id": {"type": "uuid"},
            "first_name": {"type": "first_name"},
            "last_name": {"type": "last_name"},
            "email": {"type": "email"},
            "address": {"type": "address"},
            "ssn": {"type": "ssn"},
            "birth_date": {"type": "date_past", "params": {"years": 50, "end_date": "2000-01-01"}},
            "credit_card": {"type": "credit_card_number"}
        }
    }

    Supported 'type' values (mapping to faker methods):
    - uuid, first_name, last_name, email, address, ssn, credit_card_number, date_past, date_between, etc.
    - For types like 'date_past', 'params' can be used to pass arguments to faker methods.
    - Custom types can be added by extending the `FAKER_MAPPING`.

Error Handling:
    - Exits with an error if the schema file is not found or is invalid.
    - Exits with an error if required arguments are missing.
    - Provides informative messages for invalid faker types.

Dependencies:
    - faker (install with: pip install Faker)
    - argparse (built-in)
    - json (built-in)
    - sys (built-in)
    - os (built-in)
"""

import argparse
import json
import sys
import os
from faker import Faker

# Initialize Faker
fake = Faker()

# Mapping of schema types to Faker methods
FAKER_MAPPING = {
    "uuid": fake.uuid4,
    "first_name": fake.first_name,
    "last_name": fake.last_name,
    "email": fake.email,
    "address": fake.address,
    "ssn": lambda: fake.ssn() if hasattr(fake, 'ssn') else fake.bothify(text='###-##-####'), # Fallback for SSN
    "credit_card_number": fake.credit_card_number,
    "date_past": fake.date_past,
    "date_between": fake.date_between,
    "word": fake.word,
    "sentence": fake.sentence,
    "paragraph": fake.paragraph,
    "phone_number": fake.phone_number,
    "city": fake.city,
    "state": fake.state,
    "zip_code": fake.postcode,
    "country": fake.country,
    "company": fake.company,
    "job": fake.job,
    "url": fake.url,
    "ipv4": fake.ipv4,
    "boolean": fake.boolean,
    "random_int": fake.random_int,
    "random_digit": fake.random_digit,
    "random_number": fake.random_number,
    "text": fake.text,
    "name": fake.name,
    "date_of_birth": lambda: fake.date_of_birth(minimum_age=18, maximum_age=90),
    "password": lambda: fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True),
    "iban": fake.iban,
    "swift": fake.swift,
    "currency_code": fake.currency_code,
    "license_plate": fake.license_plate,
    "mac_address": fake.mac_address,
    "user_name": fake.user_name,
    "domain_name": fake.domain_name,
    "file_extension": fake.file_extension,
    "mime_type": fake.mime_type,
    "color_name": fake.color_name,
    "hex_color": fake.hex_color,
    "rgb_color": fake.rgb_color,
    "safe_email": fake.safe_email,
    "free_email": fake.free_email,
    "company_email": fake.company_email,
    "ean13": fake.ean13,
    "ean8": fake.ean8,
    "isbn13": fake.isbn13,
    "isbn10": fake.isbn10,
    "latitude": fake.latitude,
    "longitude": fake.longitude,
    "coordinate": fake.coordinate,
    "locale": fake.locale,
    "language_code": fake.language_code,
    "country_code": fake.country_code,
    "currency_name": fake.currency_name,
    "currency_symbol": fake.currency_symbol,
    "cryptocurrency_name": fake.cryptocurrency_name,
    "cryptocurrency_code": fake.cryptocurrency_code,
    "bank_country": fake.bank_country,
    "bban": fake.bban,
    "aba": fake.aba,
    "routing_number": fake.routing_number,
    "swift8": fake.swift8,
    "swift11": fake.swift11,
    "duns_number": fake.duns_number,
    "ein": fake.ein,
    "vat_id": fake.vat_id,
    "ssn_valid": lambda: fake.ssn() if hasattr(fake, 'ssn') else fake.bothify(text='###-##-####'), # Fallback for SSN
    "passport_number": fake.passport_number,
    "driver_license": fake.license_plate, # Using license_plate as a placeholder
    "credit_card_expire": fake.credit_card_expire,
    "credit_card_security_code": fake.credit_card_security_code,
    "credit_card_provider": fake.credit_card_provider,
    "user_agent": fake.user_agent,
    "chrome": fake.chrome,
    "firefox": fake.firefox,
    "safari": fake.safari,
    "opera": fake.opera,
    "internet_explorer": fake.internet_explorer,
    "mac_platform_token": fake.mac_platform_token,
    "linux_platform_token": fake.linux_platform_token,
    "windows_platform_token": fake.windows_platform_token,
    "android_platform_token": fake.android_platform_token,
    "ios_platform_token": fake.ios_platform_token,
    "random_element": fake.random_element,
    "random_elements": fake.random_elements,
    "random_sample": fake.random_sample,
    "random_choices": fake.random_choices,
    "random_digit_not_null": fake.random_digit_not_null,
    "random_digit_not_null_or_empty": fake.random_digit_not_null_or_empty,
    "random_letter": fake.random_letter,
    "random_lowercase_letter": fake.random_lowercase_letter,
    "random_uppercase_letter": fake.random_uppercase_letter,
    "random_int_between": lambda min_val, max_val: fake.random_int(min=min_val, max=max_val),
    "random_float_between": lambda min_val, max_val: fake.pyfloat(min_value=min_val, max_value=max_val),
    "date_time_this_century": fake.date_time_this_century,
    "date_time_this_decade": fake.date_time_this_decade,
    "date_time_this_year": fake.date_time_this_year,
    "date_time_this_month": fake.date_time_this_month,
    "date_time_between": fake.date_time_between,
    "time_delta": fake.time_delta,
    "time_object": fake.time_object,
    "time_series": fake.time_series,
    "unix_time": fake.unix_time,
    "iso8601": fake.iso8601,
    "json": fake.json,
    "xml": fake.xml,
    "csv": fake.csv,
    "tsv": fake.tsv,
    "yaml": fake.yaml,
    "md5": fake.md5,
    "sha1": fake.sha1,
    "sha256": fake.sha256,
    "color": fake.color,
    "safe_color_name": fake.safe_color_name,
    "color_rgb": fake.color_rgb,
    "file_name": fake.file_name,
    "file_path": fake.file_path,
    "uri": fake.uri,
    "slug": fake.slug,
    "image_url": fake.image_url,
    "image_bytes": fake.image_bytes,
    "binary": fake.binary,
    "boolean_value": fake.boolean,
    "null_boolean": fake.null_boolean,
    "pyint": fake.pyint,
    "pyfloat": fake.pyfloat,
    "pydecimal": fake.pydecimal,
    "pylist": fake.pylist,
    "pydict": fake.pydict,
    "pyset": fake.pyset,
    "pytuple": fake.pytuple,
    "pyiterable": fake.pyiterable,
    "pyobject": fake.pyobject,
    "profile": fake.profile,
    "simple_profile": fake.simple_profile,
    "dane": fake.dane,
    "uri_extension": fake.uri_extension,
    "uri_path": fake.uri_path,
    "uri_page": fake.uri_page,
    "tld": fake.tld,
    "domain_word": fake.domain_word,
    "http_method": fake.http_method,
    "status_code": fake.status_code,
    "user_agent_name": fake.user_agent,
    "user_agent_string": fake.user_agent,
    "browser": fake.browser,
    "os": fake.os,
    "platform": fake.platform,
    "engine": fake.engine,
    "version": fake.version,
    "build_number": fake.build_number,
    "user_agent_token": fake.user_agent,
    "user_agent_header": fake.user_agent,
    "user_agent_full": fake.user_agent,
    "user_agent_short": fake.user_agent,
    "user_agent_long": fake.user_agent,
    "user_agent_random": fake.user_agent,
    "user_agent_safe": fake.user_agent,
    "user_agent_chrome": fake.chrome,
    "user_agent_firefox": fake.firefox,
    "user_agent_safari": fake.safari,
    "user_agent_opera": fake.opera,
    "user_agent_ie": fake.internet_explorer,
    "user_agent_android": fake.android_platform_token,
    "user_agent_ios": fake.ios_platform_token,
    "user_agent_linux": fake.linux_platform_token,
    "user_agent_mac": fake.mac_platform_token,
    "user_agent_windows": fake.windows_platform_token,
    "user_agent_mobile": fake.android_platform_token, # Placeholder
    "user_agent_desktop": fake.windows_platform_token, # Placeholder
    "user_agent_tablet": fake.android_platform_token, # Placeholder
    "user_agent_bot": fake.user_agent, # Placeholder
    "user_agent_crawler": fake.user_agent, # Placeholder
    "user_agent_search_engine": fake.user_agent, # Placeholder
    "user_agent_feed_reader": fake.user_agent, # Placeholder
    "user_agent_validator": fake.user_agent, # Placeholder
    "user_agent_monitor": fake.user_agent, # Placeholder
    "user_agent_test": fake.user_agent, # Placeholder
    "user_agent_custom": fake.user_agent, # Placeholder
    "user_agent_generic": fake.user_agent, # Placeholder
    "user_agent_unknown": fake.user_agent, # Placeholder
    "user_agent_empty": fake.user_agent, # Placeholder
    "user_agent_null": fake.user_agent, # Placeholder
    "user_agent_none": fake.user_agent, # Placeholder
    "user_agent_default": fake.user_agent, # Placeholder
    "user_agent_random_browser": fake.user_agent, # Placeholder
    "user_agent_random_os": fake.user_agent, # Placeholder
    "user_agent_random_platform": fake.user_agent, # Placeholder
    "user_agent_random_engine": fake.user_agent, # Placeholder
    "user_agent_random_version": fake.user_agent, # Placeholder
    "user_agent_random_build_number": fake.user_agent, # Placeholder
    "user_agent_random_user_agent": fake.user_agent, # Placeholder
    "user_agent_random_user_agent_string": fake.user_agent, # Placeholder
    "user_agent_random_user_agent_header": fake.user_agent, # Placeholder
    "user_agent_random_user_agent_full": fake.user_agent, # Placeholder
    "user_agent_random_user_agent_short": fake.user_agent, # Placeholder
    "user_agent_random_user_agent_long": fake.user_agent, # Placeholder
    "user_agent_random_user_agent_safe": fake.user_agent, # Placeholder
    "user_agent_random_user_agent_chrome": fake.chrome,
    "user_agent_random_user_agent_firefox": fake.firefox,
    "user_agent_random_user_agent_safari": fake.safari,
    "user_agent_random_user_agent_opera": fake.opera,
    "user_agent_random_user_agent_ie": fake.internet_explorer,
    "user_agent_random_user_agent_android": fake.android_platform_token,
    "user_agent_random_user_agent_ios": fake.ios_platform_token,
    "user_agent_random_user_agent_linux": fake.linux_platform_token,
    "user_agent_random_user_agent_mac": fake.mac_platform_token,
    "user_agent_random_user_agent_windows": fake.windows_platform_token,
    "user_agent_random_user_agent_mobile": fake.android_platform_token, # Placeholder
    "user_agent_random_user_agent_desktop": fake.windows_platform_token, # Placeholder
    "user_agent_random_user_agent_tablet": fake.android_platform_token, # Placeholder
    "user_agent_random_user_agent_bot": fake.user_agent, # Placeholder
    "user_agent_random_user_agent_crawler": fake.user_agent, # Placeholder
    "user_agent_random_user_agent_search_engine": fake.user_agent, # Placeholder
    "user_agent_random_user_agent_feed_reader": fake.user_agent, # Placeholder
    "user_agent_random_user_agent_validator": fake.user_agent, # Placeholder
    "user_agent_random_user_agent_monitor": fake.user_agent, # Placeholder
    "user_agent_random_user_agent_test": fake.user_agent, # Placeholder
    "user_agent_random_user_agent_custom": fake.user_agent, # Placeholder
    "user_agent_random_user_agent_generic": fake.user_agent, # Placeholder
    "user_agent_random_user_agent_unknown": fake.user_agent, # Placeholder
    "user_agent_random_user_agent_empty": fake.user_agent, # Placeholder
    "user_agent_random_user_agent_null": fake.user_agent, # Placeholder
    "user_agent_random_user_agent_none": fake.user_agent, # Placeholder
    "user_agent_random_user_agent_default": fake.user_agent, # Placeholder
}


def generate_record(schema_fields):
    """Generates a single synthetic data record based on the provided schema fields."""
    record = {}
    for field_name, field_config in schema_fields.items():
        field_type = field_config.get("type")
        params = field_config.get("params", {})

        if field_type not in FAKER_MAPPING:
            print(f"\033[91mError: Unknown faker type '{field_type}' for field '{field_name}'. Skipping.\033[0m", file=sys.stderr)
            record[field_name] = None
            continue

        try:
            generator_func = FAKER_MAPPING[field_type]
            if params:
                record[field_name] = generator_func(**params)
            else:
                record[field_name] = generator_func()
        except Exception as e:
            print(f"\033[91mError generating data for field '{field_name}' with type '{field_type}': {e}. Skipping.\033[0m", file=sys.stderr)
            record[field_name] = None
    return record

def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic data based on a JSON schema.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-s", "--schema",
        required=True,
        help="Path to the JSON schema file defining data structure and types."
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to the output JSON file. If not provided, prints to stdout."
    )
    parser.add_argument(
        "-c", "--count",
        type=int,
        default=1,
        help="Number of synthetic records to generate (default: 1)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If set, generates data but does not save to file. Prints to stdout."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output."
    )

    args = parser.parse_args()

    if not os.path.exists(args.schema):
        print(f"\033[91mError: Schema file not found at '{args.schema}'\033[0m", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.schema, 'r') as f:
            schema = json.load(f)
    except json.JSONDecodeError as e:
        print(f"\033[91mError: Invalid JSON in schema file '{args.schema}': {e}\033[0m", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\033[91mError reading schema file '{args.schema}': {e}\033[0m", file=sys.stderr)
        sys.exit(1)

    if "fields" not in schema or not isinstance(schema["fields"], dict):
        print("\033[91mError: Schema must contain a 'fields' object.\033[0m", file=sys.stderr)
        sys.exit(1)

    generated_data = []
    for i in range(args.count):
        if args.verbose:
            print(f"Generating record {i + 1}/{args.count}...")
        generated_data.append(generate_record(schema["fields"]))

    if args.dry_run or not args.output:
        print(json.dumps(generated_data, indent=2))
        if args.dry_run and args.output:
            print(f"\033[93mDry run enabled. Data not saved to '{args.output}'.\033[0m")
    else:
        try:
            with open(args.output, 'w') as f:
                json.dump(generated_data, f, indent=2)
            print(f"\033[92mSuccessfully generated {args.count} records to '{args.output}'\033[0m")
        except Exception as e:
            print(f"\033[91mError writing to output file '{args.output}': {e}\033[0m", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
