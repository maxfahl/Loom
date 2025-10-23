
import argparse
import sys

def generate_range_partition_sql(table_name, partition_key, partitions):
    """
    Generates SQL for RANGE partitioning.
    partitions: List of tuples (partition_name, lower_bound, upper_bound)
    """
    sql_statements = []
    sql_statements.append(f"CREATE TABLE {table_name} (")
    sql_statements.append(f"    -- Define your columns here, e.g., id INT, data TEXT, {partition_key} DATE
")
    sql_statements.append(f") PARTITION BY RANGE ({partition_key});\n")

    for p_name, lower, upper in partitions:
        sql_statements.append(f"CREATE TABLE {table_name}_{p_name}")
        sql_statements.append(f"    PARTITION OF {table_name} FOR VALUES FROM ('{lower}') TO ('{upper}');")

    sql_statements.append(f"\n-- Optional: Create a default partition for values outside defined ranges")
    sql_statements.append(f"-- CREATE TABLE {table_name}_default")
    sql_statements.append(f"--     PARTITION OF {table_name} DEFAULT;")

    return "\n".join(sql_statements)

def generate_list_partition_sql(table_name, partition_key, partitions):
    """
    Generates SQL for LIST partitioning.
    partitions: List of tuples (partition_name, list_of_values)
    """
    sql_statements = []
    sql_statements.append(f"CREATE TABLE {table_name} (")
    sql_statements.append(f"    -- Define your columns here, e.g., id INT, data TEXT, {partition_key} TEXT
")
    sql_statements.append(f") PARTITION BY LIST ({partition_key});\n")

    for p_name, values in partitions:
        values_str = ', '.join([f"'{v}'" for v in values])
        sql_statements.append(f"CREATE TABLE {table_name}_{p_name}")
        sql_statements.append(f"    PARTITION OF {table_name} FOR VALUES IN ({values_str});")

    sql_statements.append(f"\n-- Optional: Create a default partition for values not in any list")
    sql_statements.append(f"-- CREATE TABLE {table_name}_default")
    sql_statements.append(f"--     PARTITION OF {table_name} DEFAULT;")

    return "\n".join(sql_statements)

def generate_hash_partition_sql(table_name, partition_key, num_partitions):
    """
    Generates SQL for HASH partitioning.
    num_partitions: Integer, number of hash partitions
    """
    sql_statements = []
    sql_statements.append(f"CREATE TABLE {table_name} (")
    sql_statements.append(f"    -- Define your columns here, e.g., id INT, data TEXT, {partition_key} INT
")
    sql_statements.append(f") PARTITION BY HASH ({partition_key});\n")

    for i in range(num_partitions):
        sql_statements.append(f"CREATE TABLE {table_name}_p{i}")
        sql_statements.append(f"    PARTITION OF {table_name} FOR VALUES WITH (MODULUS {num_partitions}, REMAINDER {i});")

    return "\n".join(sql_statements)

def main():
    parser = argparse.ArgumentParser(
        description="Generates SQL DDL for PostgreSQL declarative partitioning.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "table_name",
        help="The name of the table to partition."
    )
    parser.add_argument(
        "partition_key",
        help="The column to use as the partition key."
    )
    parser.add_argument(
        "--type",
        choices=["range", "list", "hash"],
        required=True,
        help="Type of partitioning: range, list, or hash."
    )
    parser.add_argument(
        "--partitions",
        nargs='+',
        help="\n"
             "For RANGE: List of partition definitions as 'name:lower_bound:upper_bound'.\n"
             "  Example: 'q1:2023-01-01:2023-04-01' 'q2:2023-04-01:2023-07-01'\n"
             "For LIST: List of partition definitions as 'name:value1,value2,...'.\n"
             "  Example: 'east:NY,MA' 'west:CA,OR'\n"
             "For HASH: Single integer representing the number of partitions.\n"
             "  Example: '4'"
    )

    args = parser.parse_args()

    sql_output = ""

    if args.type == "range":
        if not args.partitions or not all(len(p.split(':')) == 3 for p in args.partitions):
            print("Error: For RANGE partitioning, --partitions must be 'name:lower_bound:upper_bound'.")
            sys.exit(1)
        parsed_partitions = [p.split(':') for p in args.partitions]
        sql_output = generate_range_partition_sql(args.table_name, args.partition_key, parsed_partitions)
    elif args.type == "list":
        if not args.partitions or not all(len(p.split(':')) == 2 for p in args.partitions):
            print("Error: For LIST partitioning, --partitions must be 'name:value1,value2,...'.")
            sys.exit(1)
        parsed_partitions = []
        for p in args.partitions:
            name, values_str = p.split(':')
            parsed_partitions.append((name, values_str.split(',')))
        sql_output = generate_list_partition_sql(args.table_name, args.partition_key, parsed_partitions)
    elif args.type == "hash":
        if not args.partitions or len(args.partitions) != 1 or not args.partitions[0].isdigit():
            print("Error: For HASH partitioning, --partitions must be a single integer (number of partitions).")
            sys.exit(1)
        num_partitions = int(args.partitions[0])
        sql_output = generate_hash_partition_sql(args.table_name, args.partition_key, num_partitions)

    print(sql_output)

if __name__ == "__main__":
    main()
