#!/usr/bin/env python3

"""
Database Replication Status Checker

This script checks the replication status of a PostgreSQL database and reports
any lag or issues. It's designed to be used in HA monitoring systems to ensure
data consistency and availability across replicas.

Usage:
    python3 db_replication_check.py --db-type postgres \
        --host localhost --port 5432 --user replicator --password mysecretpassword \
        --dbname mydb --max-lag 10
    python3 db_replication_check.py -h # For help

Requirements:
    - psycopg2 (for PostgreSQL): pip install psycopg2-binary

Features:
- Connects to a PostgreSQL database.
- Checks if the database is a replica and its replication status.
- Reports replication lag in seconds.
- Exits with a non-zero status code if replication lag exceeds a threshold or on errors.
"""

import argparse
import sys

try:
    import psycopg2
    from psycopg2 import OperationalError, Error
except ImportError:
    print("Error: 'psycopg2-binary' library not found. Please install it: pip install psycopg2-binary", file=sys.stderr)
    sys.exit(1)

def check_postgres_replication(host, port, user, password, dbname, max_lag_seconds):
    conn = None
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname,
            connect_timeout=5
        )
        cur = conn.cursor()

        # Check if it's a replica
        cur.execute("SELECT pg_is_in_recovery();")
        is_replica = cur.fetchone()[0]

        if not is_replica:
            print("✅ Database is a primary instance. No replication lag to check.")
            return True

        # Get replication status for replicas
        cur.execute("SELECT client_addr, state, sync_state, sync_priority, pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS lag_bytes FROM pg_stat_replication;")
        replication_info = cur.fetchall()

        if not replication_info:
            print("❌ Database is a replica but no active replication partners found.", file=sys.stderr)
            return False

        all_replicas_healthy = True
        for rep in replication_info:
            client_addr, state, sync_state, sync_priority, lag_bytes = rep
            lag_seconds = lag_bytes / 1024 / 1024 / 1024 * 8 # Rough conversion from bytes to seconds, assuming 8MB/s WAL generation
            # This conversion is highly dependent on WAL generation rate and is an approximation.
            # A more accurate lag would involve comparing timestamps or specific LSNs.

            print(f"Replica {client_addr}: State={state}, Sync State={sync_state}, Lag (bytes)={lag_bytes}, Estimated Lag (seconds)={lag_seconds:.2f}")

            if state != 'streaming' or sync_state not in ('sync', 'async'):
                print(f"❌ Replica {client_addr} is not in a healthy streaming state.", file=sys.stderr)
                all_replicas_healthy = False
            if lag_seconds > max_lag_seconds:
                print(f"❌ Replica {client_addr} lag ({lag_seconds:.2f}s) exceeds max allowed lag ({max_lag_seconds}s).", file=sys.stderr)
                all_replicas_healthy = False

        return all_replicas_healthy

    except OperationalError as e:
        print(f"❌ Database connection failed: {e}", file=sys.stderr)
        return False
    except Error as e:
        print(f"❌ Database error: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}", file=sys.stderr)
        return False
    finally:
        if conn:
            conn.close()

def main():
    parser = argparse.ArgumentParser(
        description="Check PostgreSQL database replication status.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--db-type",
        choices=["postgres"], # Extend with 'mysql' etc. as needed
        required=True,
        help="Type of database to check (e.g., postgres)."
    )
    parser.add_argument(
        "--host",
        required=True,
        help="Database host."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5432,
        help="Database port. Default: 5432 for PostgreSQL."
    )
    parser.add_argument(
        "--user",
        required=True,
        help="Database user."
    )
    parser.add_argument(
        "--password",
        required=True,
        help="Database password."
    )
    parser.add_argument(
        "--dbname",
        required=True,
        help="Database name."
    )
    parser.add_argument(
        "--max-lag",
        type=int,
        default=60,
        help="Maximum allowed replication lag in seconds before reporting failure. Default: 60"
    )

    args = parser.parse_args()

    if args.db_type == "postgres":
        if not check_postgres_replication(
            args.host, args.port, args.user, args.password, args.dbname, args.max_lag
        ):
            sys.exit(1)
    else:
        print(f"Error: Database type '{args.db_type}' not supported yet.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
