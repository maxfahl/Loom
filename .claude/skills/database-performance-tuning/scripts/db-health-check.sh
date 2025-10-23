#!/bin/bash

# db-health-check.sh
#
# Description:
#   Performs a series of health checks on a PostgreSQL database, gathering key metrics
#   like active connections, locks, buffer hit ratio, and disk I/O. It provides a
#   summary report and highlights potential areas of concern.
#
# Usage:
#   ./db-health-check.sh
#   DB_HOST=myhost DB_USER=admin DB_NAME=prod_db ./db-health-check.sh
#
# Requirements:
#   - psql (PostgreSQL client) must be installed and accessible in PATH.
#
# Configuration:
#   DB_HOST: Database host (default: localhost)
#   DB_PORT: Database port (default: 5432)
#   DB_USER: Database user (default: postgres)
#   DB_NAME: Database name (default: postgres)
#   DB_PASSWORD: Database password (optional, will prompt if not set)
#
# Features:
#   - Gathers and displays various PostgreSQL performance metrics.
#   - Highlights metrics that might indicate issues.
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

# --- Colors for output ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# --- Functions ---

# Function to display help message
show_help() {
  echo "Usage: $0"
  echo ""
  echo "  Performs a series of health checks on a PostgreSQL database."
  echo ""
  echo "Environment Variables (for PostgreSQL connection):"
  echo "  DB_HOST      Database host (default: localhost)"
  echo "  DB_PORT      Database port (default: 5432)"
  echo "  DB_USER      Database user (default: postgres)"
  echo "  DB_NAME      Database name (default: postgres)"
  echo "  DB_PASSWORD  Database password (optional, will prompt if not set)"
  echo ""
  echo "Example:"
  echo "  ./db-health-check.sh"
  echo "  DB_USER=myuser DB_NAME=mydb ./db-health-check.sh"
  echo ""
  echo "Note: This script is tailored for PostgreSQL. For other databases, commands would differ."
}

# Function to run a psql query and return result
run_psql_query() {
  local query="$1"
  local result
  if [ -n "$DB_PASSWORD" ]; then
    PGPASSWORD="$DB_PASSWORD" result=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "$query" 2>&1)
  else
    result=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "$query" 2>&1)
  fi
  echo "$result" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' # Trim whitespace
}

# --- Main Script Logic ---

# Check if psql is installed
if ! command -v psql &> /dev/null; then
  echo -e "${RED}Error: 'psql' command not found. Please install PostgreSQL client.${NC}"
  exit 1
fi

# Check for help flag
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  show_help
  exit 0
fi

echo -e "${BLUE}--- PostgreSQL Database Health Check ---${NC}"
echo -e "${BLUE}Database: ${DB_USER}@${DB_HOST}:${DB_PORT}/${DB_NAME}${NC}"
echo -e "${BLUE}Timestamp: $(date)${NC}"
echo ""

# --- 1. Connection Status ---
echo -e "${YELLOW}1. Connection Status:${NC}"
TOTAL_CONNECTIONS=$(run_psql_query "SELECT count(*) FROM pg_stat_activity;")
ACTIVE_CONNECTIONS=$(run_psql_query "SELECT count(*) FROM pg_stat_activity WHERE state = 'active';")
IDLE_IN_TXN_CONNECTIONS=$(run_psql_query "SELECT count(*) FROM pg_stat_activity WHERE state = 'idle in transaction';")
MAX_CONNECTIONS=$(run_psql_query "SHOW max_connections;")

if [[ -z "$TOTAL_CONNECTIONS" || -z "$MAX_CONNECTIONS" ]]; then
  echo -e "${RED}  Error: Could not retrieve connection stats. Check database connectivity and permissions.${NC}"
  exit 1
fi

echo "  Total Connections: ${TOTAL_CONNECTIONS} / ${MAX_CONNECTIONS}"
echo "  Active Connections: ${ACTIVE_CONNECTIONS}"
echo "  Idle in Transaction: ${IDLE_IN_TXN_CONNECTIONS}"

if (( $(echo "${TOTAL_CONNECTIONS} > ${MAX_CONNECTIONS} * 0.8" | bc -l) )); then
  echo -e "${RED}  Warning: Total connections are over 80% of max_connections!${NC}"
elif (( $(echo "${TOTAL_CONNECTIONS} > ${MAX_CONNECTIONS} * 0.6" | bc -l) )); then
  echo -e "${YELLOW}  Note: Total connections are over 60% of max_connections.${NC}"
fi

if (( ${IDLE_IN_TXN_CONNECTIONS} > 0 )); then
  echo -e "${RED}  Warning: There are ${IDLE_IN_TXN_CONNECTIONS} connections 'idle in transaction'. This can lead to bloat and resource exhaustion!${NC}"
fi
echo ""

# --- 2. Locks ---
echo -e "${YELLOW}2. Locks:${NC}"
BLOCKED_QUERIES=$(run_psql_query "SELECT count(*) FROM pg_locks WHERE granted = false;")
LONG_RUNNING_LOCKS=$(run_psql_query "SELECT count(*) FROM pg_locks pl JOIN pg_stat_activity psa ON pl.pid = psa.pid WHERE pl.granted = false AND age(now(), psa.query_start) > INTERVAL '1 minute';")

echo "  Blocked Queries: ${BLOCKED_QUERIES}"
if (( ${BLOCKED_QUERIES} > 0 )); then
  echo -e "${RED}  Warning: ${BLOCKED_QUERIES} queries are currently blocked!${NC}"
fi
if (( ${LONG_RUNNING_LOCKS} > 0 )); then
  echo -e "${RED}  Warning: ${LONG_RUNNING_LOCKS} queries have been blocked for over 1 minute!${NC}"
fi
echo ""

# --- 3. Cache Hit Ratio (for shared buffers) ---
echo -e "${YELLOW}3. Cache Hit Ratio (Shared Buffers):${NC}"
BUFFER_HITS=$(run_psql_query "SELECT sum(blks_hit) FROM pg_stat_database;")
BUFFER_READS=$(run_psql_query "SELECT sum(blks_read) FROM pg_stat_database;")

if [[ -n "$BUFFER_HITS" && -n "$BUFFER_READS" && "$BUFFER_READS" -ne 0 ]]; then
  HIT_RATIO=$(echo "scale=2; (${BUFFER_HITS} * 100) / (${BUFFER_HITS} + ${BUFFER_READS})" | bc -l)
  echo "  Buffer Hit Ratio: ${HIT_RATIO}%"
  if (( $(echo "${HIT_RATIO} < 90" | bc -l) )); then
    echo -e "${RED}  Warning: Buffer hit ratio is below 90%. Consider increasing shared_buffers.${NC}"
  elif (( $(echo "${HIT_RATIO} < 95" | bc -l) )); then
    echo -e "${YELLOW}  Note: Buffer hit ratio is below 95%. May be worth investigating.${NC}"
  fi
else
  echo "  Buffer Hit Ratio: N/A (not enough data or error)"
fi
echo ""

# --- 4. Disk I/O (Table/Index Scans) ---
echo -e "${YELLOW}4. Disk I/O (Table/Index Scans):${NC}"
SEQ_SCANS=$(run_psql_query "SELECT sum(seq_scan) FROM pg_stat_all_tables;")
IDX_SCANS=$(run_psql_query "SELECT sum(idx_scan) FROM pg_stat_all_tables;")

echo "  Total Sequential Scans: ${SEQ_SCANS}"
echo "  Total Index Scans: ${IDX_SCANS}"

if [[ -n "$SEQ_SCANS" && -n "$IDX_SCANS" && "$SEQ_SCANS" -ne 0 ]]; then
  SCAN_RATIO=$(echo "scale=2; (${IDX_SCANS} * 100) / (${SEQ_SCANS} + ${IDX_SCANS})" | bc -l)
  echo "  Index Scan Ratio (vs. Total Scans): ${SCAN_RATIO}%"
  if (( $(echo "${SCAN_RATIO} < 80" | bc -l) )); then
    echo -e "${RED}  Warning: Index scan ratio is below 80%. Many sequential scans might indicate missing indexes or inefficient queries.${NC}"
  fi
else
  echo "  Scan Ratio: N/A (not enough data or error)"
fi
echo ""

# --- 5. Long Running Queries ---
echo -e "${YELLOW}5. Long Running Queries (Top 5 > 10 seconds):${NC}"
LONG_QUERIES=$(run_psql_query "SELECT pid, usename, application_name, client_addr, query_start, age(now(), query_start) AS duration, query FROM pg_stat_activity WHERE state = 'active' AND age(now(), query_start) > INTERVAL '10 seconds' ORDER BY duration DESC LIMIT 5;")

if [ -n "$LONG_QUERIES" ]; then
  echo -e "${RED}  Warning: The following queries have been running for over 10 seconds:${NC}"
  echo "${LONG_QUERIES}"
else
  echo "  No active queries running for more than 10 seconds."
fi
echo ""

echo -e "${BLUE}--- Health Check Complete ---${NC}"
exit 0
