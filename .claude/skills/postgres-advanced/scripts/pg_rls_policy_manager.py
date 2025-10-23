
import argparse
import os
import sys

try:
    import psycopg2
    from psycopg2 import sql
except ImportError:
    print("Error: psycopg2 not found. Please install it using: pip install psycopg2-binary")
    sys.exit(1)

def get_db_connection(dbname, user, password, host, port):
    """
    Establishes a connection to the PostgreSQL database.
    """
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)

def create_policy(cursor, table_name, policy_name, roles, command, using_expr, with_check_expr):
    """
    Generates and executes a CREATE POLICY statement.
    """
    roles_str = ', '.join(roles) if roles else 'PUBLIC'
    command_str = f"FOR {command}" if command else ""
    using_clause = f"USING ({using_expr})" if using_expr else ""
    with_check_clause = f"WITH CHECK ({with_check_expr})" if with_check_expr else ""

    policy_sql = f"CREATE POLICY {policy_name} ON {table_name} " \
                 f"{command_str} TO {roles_str} {using_clause} {with_check_clause};"

    enable_rls_sql = f"ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY;"

    print(f"\n--- Generated SQL for RLS Policy ---")
    print(enable_rls_sql)
    print(policy_sql)
    print("\n--- To apply, execute the above SQL statements in your PostgreSQL client. ---")

    # In a real scenario, you might offer to execute this if not in dry-run
    # try:
    #     cursor.execute(enable_rls_sql)
    #     cursor.execute(policy_sql)
    #     print("Policy created and RLS enabled.")
    # except psycopg2.Error as e:
    #     print(f"Error applying policy: {e}")

def view_policies(cursor, table_name=None):
    """
    Views existing RLS policies.
    """
    print("\n--- Existing RLS Policies ---")
    query = "SELECT policyname, perm_type, roles, qual, with_check FROM pg_policies"
    if table_name:
        query += f" WHERE tablename = '{table_name}'"
    query += ";"

    cursor.execute(query)
    policies = cursor.fetchall()

    if policies:
        for policyname, perm_type, roles, qual, with_check in policies:
            print(f"Policy Name: {policyname}")
            print(f"  Table: {table_name if table_name else 'All'}")
            print(f"  Perm Type: {perm_type}")
            print(f"  Roles: {roles}")
            print(f"  Using: {qual}")
            print(f"  With Check: {with_check}")
            print("----------------------------------")
    else:
        print(f"No RLS policies found for table '{table_name}'" if table_name else "No RLS policies found.")

def audit_table_rls(cursor, table_name):
    """
    Audits RLS status for a given table.
    """
    print(f"\n--- RLS Audit for Table: {table_name} ---")
    cursor.execute(f"SELECT relrowsecurity FROM pg_class WHERE relname = '{table_name}';")
    result = cursor.fetchone()

    if result is None:
        print(f"Error: Table '{table_name}' not found.")
        return

    rls_enabled = result[0]
    print(f"Row Level Security enabled: {rls_enabled}")

    if rls_enabled:
        print("Existing policies:")
        view_policies(cursor, table_name)
    else:
        print(f"RLS is not enabled for table '{table_name}'. Use 'ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY;' to enable it.")

def main():
    parser = argparse.ArgumentParser(
        description="Manages PostgreSQL Row-Level Security (RLS) policies.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--dbname", required=True,
        help="Database name."
    )
    parser.add_argument(
        "--user", required=True,
        help="Database user."
    )
    parser.add_argument(
        "--password", default=os.getenv("PGPASSWORD"),
        help="Database password. Can be provided via PGPASSWORD environment variable."
    )
    parser.add_argument(
        "--host", default="localhost",
        help="Database host (default: localhost)."
    )
    parser.add_argument(
        "--port", type=int, default=5432,
        help="Database port (default: 5432)."
    )

    subparsers = parser.add_subparsers(dest='action', required=True, help='Action to perform')

    # Create policy subparser
    create_parser = subparsers.add_parser('create', help='Create a new RLS policy')
    create_parser.add_argument('--table', required=True, help='Table name for the policy')
    create_parser.add_argument('--name', required=True, help='Policy name')
    create_parser.add_argument('--roles', nargs='+', help='Roles to apply the policy to (e.g., app_user admin_user). Defaults to PUBLIC.')
    create_parser.add_argument('--command', choices=['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'ALL'], default='ALL', help='Command type for the policy')
    create_parser.add_argument('--using', help='USING expression (e.g., \'user_id = current_setting("app.user_id")::int\')')
    create_parser.add_argument('--with-check', help='WITH CHECK expression (e.g., \'user_id = current_setting("app.user_id")::int\')')

    # View policies subparser
    view_parser = subparsers.add_parser('view', help='View existing RLS policies')
    view_parser.add_argument('--table', help='Optional: Table name to filter policies')

    # Audit RLS subparser
    audit_parser = subparsers.add_parser('audit', help='Audit RLS status for a table')
    audit_parser.add_argument('--table', required=True, help='Table name to audit')

    args = parser.parse_args()

    conn = get_db_connection(args.dbname, args.user, args.password, args.host, args.port)
    cursor = conn.cursor()

    if args.action == 'create':
        create_policy(cursor, args.table, args.name, args.roles, args.command, args.using, args.with_check)
    elif args.action == 'view':
        view_policies(cursor, args.table)
    elif args.action == 'audit':
        audit_table_rls(cursor, args.table)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
