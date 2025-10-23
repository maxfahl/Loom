#!/bin/bash

# analyze-query-plan.sh
#
# Description:
#   Automates running EXPLAIN (or equivalent) for a given SQL query against a PostgreSQL database
#   and provides a formatted, human-readable output, highlighting potential performance issues
#   like full table scans.
#
# Usage:
#   ./analyze-query-plan.sh "SELECT * FROM users WHERE status = 'active';"
#   DB_HOST=localhost DB_PORT=5432 DB_USER=admin DB_NAME=mydb DB_PASSWORD=password ./analyze-query-plan.sh "SELECT id, name FROM products WHERE price > 100 ORDER BY name;"
#
# Requirements:
#   - psql (PostgreSQL client) must be installed and accessible in PATH.
#   - Database connection details can be provided via environment variables or directly in the script.
#
# Configuration:
#   DB_HOST: Database host (default: localhost)
#   DB_PORT: Database port (default: 5432)
#   DB_USER: Database user (default: postgres)
#   DB_NAME: Database name (default: postgres)
#   DB_PASSWORD: Database password (optional, will prompt if not set)
#
# Features:
#   - Accepts SQL query as a command-line argument.
#   - Uses environment variables for database connection.
#   - Highlights "Seq Scan" (full table scan) in the output.
#   - Provides basic error handling.
#
# Cross-platform compatibility:
#   - Designed for Unix-like systems (Linux, macOS). For Windows, consider using WSL or adapting for PowerShell.

# --- Configuration ---
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_USER="${DB_USER:-postgres}"
DB_NAME="${DB_NAME:-postgres}"
DB_PASSWORD="${DB_PASSWORD}" # Will prompt if not set

# --- Functions ---

# Function to display help message
show_help() {
  echo "Usage: $0 \"<SQL_QUERY>\""
  echo ""
  echo "  Automates running EXPLAIN for a SQL query and highlights potential issues."
  echo ""
  echo "Arguments:"
  echo "  <SQL_QUERY>  The SQL query to analyze with EXPLAIN."
  echo ""
  echo "Environment Variables (for PostgreSQL connection):"
  echo "  DB_HOST      Database host (default: localhost)"
  echo "  DB_PORT      Database port (default: 5432)"
  echo "  DB_USER      Database user (default: postgres)"
  echo "  DB_NAME      Database name (default: postgres)"
  echo "  DB_PASSWORD  Database password (optional, will prompt if not set)"
  echo ""
  echo "Example:"
  echo "  ./analyze-query-plan.sh \"SELECT * FROM users WHERE status = 'active';\""
  echo "  DB_USER=myuser DB_NAME=mydb ./analyze-query-plan.sh \"SELECT COUNT(*) FROM orders WHERE created_at < NOW() - INTERVAL '1 year';\""
  echo ""
  echo "Note: For other databases (MySQL, SQL Server), you would need to adapt the 'psql' command"
  echo "      and the EXPLAIN syntax accordingly. This script is tailored for PostgreSQL."
}

# Function to run EXPLAIN and format output
run_explain() {
  local query="$1"
  local explain_command="EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) ${query}"

  echo "--- Analyzing Query Plan ---"
  echo "Query: ${query}"
  echo "Database: ${DB_USER}@${DB_HOST}:${DB_PORT}/${DB_NAME}"
  echo "----------------------------"
  echo ""

  # Set PGPASSWORD if available, otherwise psql will prompt
  if [ -n "$DB_PASSWORD" ]; then
    PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "$explain_command" 2>&1 |
    awk '{
      if ($0 ~ /Seq Scan/) {
        print "\033[0;31m" $0 "\033[0m" # Red for Seq Scan
      } else if ($0 ~ /Index Scan/) {
        print "\033[0;32m" $0 "\033[0m" # Green for Index Scan
      } else {
        print $0
      }
    }'
  else
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "$explain_command" 2>&1 |
    awk '{
      if ($0 ~ /Seq Scan/) {
        print "\033[0;31m" $0 "\033[0m" # Red for Seq Scan
      } else if ($0 ~ /Index Scan/) {
        print "\033[0;32m" $0 "\033[0m" # Green for Index Scan
      } else {
        print $0
      }
    }'
  fi

  local exit_code=${PIPESTATUS[0]} # Get exit code of psql
  if [ $exit_code -ne 0 ]; then
    echo ""
    echo -e "\033[0;31mError: Failed to execute EXPLAIN command or connect to database.\033[0m"
    echo -e "\033[0;31mPlease check your SQL query, database connection details, and 'psql' installation.\033[0m"
    return 1
  fi
  return 0
}

# --- Main Script Logic ---

# Check if psql is installed
if ! command -v psql &> /dev/null; then
  echo -e "\033[0;31mError: 'psql' command not found. Please install PostgreSQL client.\033[0m"
  exit 1
fi

# Check for arguments
if [ "$#" -eq 0 ]; then
  show_help
  exit 1
fi

# Check if the first argument is a help flag
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  show_help
  exit 0
fi

SQL_QUERY="$1"

# Run the EXPLAIN command
run_explain "$SQL_QUERY"
exit $?
