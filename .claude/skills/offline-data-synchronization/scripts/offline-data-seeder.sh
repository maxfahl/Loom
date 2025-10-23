#!/bin/bash

# offline-data-seeder.sh: Populates a local database with mock data for testing offline functionality.
#
# This script generates a JSON file containing mock data based on a simple schema.
# The generated JSON can then be imported into your local mobile database (e.g., SQLite, Realm, Core Data).
#
# Usage:
#   ./offline-data-seeder.sh -n 100 -o users_data.json
#   ./offline-data-seeder.sh --records 50 --output products_data.json
#
# After generation, you would typically use your application's data import
# mechanism or a database-specific tool to load this JSON data.

# --- Configuration ---
DEFAULT_RECORDS=10
DEFAULT_OUTPUT_FILE="mock_data.json"

# --- Helper Functions ---
function show_help() {
    echo "Usage: $(basename "$0") [OPTIONS]"
    echo "Generate mock data for local database seeding."
    echo ""
    echo "Options:"
    echo "  -n, --records <NUMBER>    Number of records to generate (default: ${DEFAULT_RECORDS})"
    echo "  -o, --output <FILE>       Output JSON file name (default: ${DEFAULT_OUTPUT_FILE})"
    echo "  -t, --type <TYPE>         Type of data to generate (e.g., users, products). Default: users"
    echo "  -h, --help                Display this help message"
    echo ""
    echo "Example:"
    echo "  $(basename "$0") -n 50 -o test_users.json -t users"
    echo "  $(basename "$0") --records 20 --output test_products.json --type products"
    echo ""
    echo "Note: This script requires 'jq' for JSON manipulation."
    exit 0
}

function generate_user_data() {
    local num_records=$1
    local output_file=$2
    echo "Generating ${num_records} user records to ${output_file}..."

    echo "[" > "${output_file}"
    for i in $(seq 1 $num_records);
    do
        USER_ID=$(uuidgen | head -c 8)
        USER_NAME="User_$(printf %03d $i)"
        USER_EMAIL="user${i}@example.com"
        USER_AGE=$(( RANDOM % 50 + 18 )) # Age between 18 and 67
        USER_TIMESTAMP=$(date +%s)

        jq -n \
            --arg id "$USER_ID" \
            --arg name "$USER_NAME" \
            --arg email "$USER_EMAIL" \
            --argjson age "$USER_AGE" \
            --argjson timestamp "$USER_TIMESTAMP" \
            '{id: $id, name: $name, email: $email, age: $age, timestamp: $timestamp}' >> "${output_file}"

        if [ $i -lt $num_records ]; then
            echo "," >> "${output_file}"
        fi
    done
    echo "]" >> "${output_file}"
    echo "Generated ${num_records} user records."
}

function generate_product_data() {
    local num_records=$1
    local output_file=$2
    echo "Generating ${num_records} product records to ${output_file}..."

    echo "[" > "${output_file}"
    for i in $(seq 1 $num_records);
    do
        PRODUCT_ID=$(uuidgen | head -c 8)
        PRODUCT_NAME="Product_$(printf %03d $i)"
        PRODUCT_PRICE=$(echo "scale=2; $(( RANDOM % 10000 + 100 )) / 100" | bc)
        PRODUCT_STOCK=$(( RANDOM % 1000 ))
        PRODUCT_TIMESTAMP=$(date +%s)

        jq -n \
            --arg id "$PRODUCT_ID" \
            --arg name "$PRODUCT_NAME" \
            --argjson price "$PRODUCT_PRICE" \
            --argjson stock "$PRODUCT_STOCK" \
            --argjson timestamp "$PRODUCT_TIMESTAMP" \
            '{id: $id, name: $name, price: $price, stock: $stock, timestamp: $timestamp}' >> "${output_file}"

        if [ $i -lt $num_records ]; then
            echo "," >> "${output_file}"
        fi
    done
    echo "]" >> "${output_file}"
    echo "Generated ${num_records} product records."
}

# --- Main Logic ---
NUM_RECORDS=${DEFAULT_RECORDS}
OUTPUT_FILE=${DEFAULT_OUTPUT_FILE}
DATA_TYPE="users"

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -n|--records)
            NUM_RECORDS="$2"
            shift # past argument
            shift # past value
            ;; 
        -o|--output)
            OUTPUT_FILE="$2"
            shift # past argument
            shift # past value
            ;; 
        -t|--type)
            DATA_TYPE="$2"
            shift # past argument
            shift # past value
            ;; 
        -h|--help)
            show_help
            ;; 
        *)
            echo "Unknown option: $1"
            show_help
            ;; 
    esac
done

# Validate input
if ! [[ "$NUM_RECORDS" =~ ^[0-9]+$ ]]; then
    echo "Error: --records must be a number." >&2
    show_help
fi

if ! command -v jq &> /dev/null; then
    echo "Error: 'jq' is not installed. Please install it to run this script." >&2
    exit 1
fi

if ! command -v uuidgen &> /dev/null; then
    echo "Error: 'uuidgen' is not installed. Please install it to run this script." >&2
    exit 1
fi

# Generate data based on type
case "$DATA_TYPE" in
    users)
        generate_user_data "$NUM_RECORDS" "$OUTPUT_FILE"
        ;; 
    products)
        generate_product_data "$NUM_RECORDS" "$OUTPUT_FILE"
        ;; 
    *)
        echo "Error: Unsupported data type '$DATA_TYPE'. Supported types: users, products." >&2
        show_help
        ;; 
esac

echo "\nData generation complete. You can now import '${OUTPUT_FILE}' into your local database."
echo "For example, if using SQLite, you might write a small script to parse this JSON and insert into tables."
